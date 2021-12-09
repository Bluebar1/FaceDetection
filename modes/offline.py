"""
Allow specifying a folder path containing the large set of images, the system should then run 
the face detection on these images (1-by-1), save the images with detected faces in another folder, 
also save the other related data to calculate the accuracy and efficiency, etc.

Arguments:
    Path to folder containing photos
    Name of Algorithm to use
"""

import config
import utils
import os, sys
import cv2
import json

from tqdm import tqdm
from mtcnn_cv2 import MTCNN
from retinaface import RetinaFace
from pathlib import Path


from algorithms import mtcnn
from algorithms import haar_cascade
from algorithms import retina
import threading

class myThread (threading.Thread):
    def __init__(self, callingScript, args):
        threading.Thread.__init__(self)
        self.args = args
        self.callingScript = callingScript
    def run(self):
        args = self.args
        callingScript = self.callingScript
        callingScript.updateOfflineProgress(0, "")
        callingScript.root.ids.offlineRunTime.text = "Run Time:"
        callingScript.root.ids.offlineAvgRunTime.text = "Avg. Run Time:"
        callingScript.root.ids.offlineFaceCounted.text = "Faces Detected:"
        callingScript.root.ids.offlineAvgFaceCounted.text = "Avg. Faces Detected:"

        algorithm = args[0]
        dataset = args[1] 
        print("Dataset is: " + dataset) 
        workingFolder = args[4]
        offlineOutputPath = workingFolder + config.offlineOutputPath
        offlineDataLocation = workingFolder + '\\results\\offline.json'
        offlineLatexLocation = workingFolder + '\\results\\latex.txt'
        #print("Reached 1")
        os.makedirs(offlineOutputPath, exist_ok=True)
        os.makedirs(workingFolder + '\\results\\', exist_ok=True)

        if args[2] == '':
            limit = 0
        else:
            limit = int(args[2])
        
        markName = args[3]  
    
        #NOTE (SEAN VONNEGUT): Was best to get the whole path from kivy so I did not use config.markingsLoc. Let me know if it is needed.
        path = dataset
        markPath = dataset + '/' + markName + '.json' #JSON file must be inside the dataset folder if mark name is included.

        isTrained = False
        #print("Reached 2")
        if markName != "":
            isTrained = True
            data = utils.loadJSON(markPath)
            i = 0

        # if os.path.isfile(markPath) :
        #     data = utils.loadJSON(markPath)
        # else :
        #     data = []

        delPreviousResults(offlineOutputPath, offlineDataLocation)

        facesDetected = 0
        totalRuntime = 0
        totalImagesChecked = 0 #Counted instead of getting length of list since some files may have a invaild file type
        #print("Reached 3")
        if isTrained :
            totalFalseDetections = 0
            totalAccuracy = 0
        else:
            totalFalseDetections = 'na'
            totalAccuracy = 'na'
        #print("Reached 4")
        # Gets list paths to images in selected dataset
        images = os.listdir(path)
        
        # Shrink list to limit arg
        if limit != 0 : del images[limit:]

        totalNumberOfFiles = len(images)
        # Initialize algorithm
        if algorithm == 'mtcnn' :
            det = MTCNN()
        elif algorithm == 'haar' :
            if hasattr(sys, '_MEIPASS'): # if it's in EXE form
                det = cv2.CascadeClassifier(sys._MEIPASS + '\\haarcascade_frontalface_default.xml')
            else : 
                det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        elif algorithm == 'retina' :
            model = RetinaFace.build_model()
        #print("Reached 5")

        for filename in tqdm(images) :
            print("Processing next image")
            if (filename[-3:] == "png") | (filename[-3:] == "jpg"): #Accepted file types
                currentScanProgress = (totalImagesChecked+1) / totalNumberOfFiles
                callingScript.updateOfflineProgress(currentScanProgress, filename)
                #callingScript.root.ids.offlineModeCurrentProgress.value = currentScanProgress
                #callingScript.root.ids.offlineModeCurrentFile.text = filename
                tic = utils.currentTime()

                if algorithm == 'mtcnn' :
                    result = mtcnn.getResult(path + '/' + filename, det)
                elif algorithm == 'haar' :
                    result = haar_cascade.getResult(path + '/' + filename, det)
                elif algorithm == 'retina' :
                    result = retina.getResult(path + '/' + filename, model)

                toc = utils.currentTime()

                if isTrained :
                    marks = data[i]
                    i+=1
                    isSuccess = runTest(result, marks, filename, workingFolder)
                else : 
                    isSuccess = 'na'

                result.setAny(
                    resultSaveLoc=offlineOutputPath,
                    algorithm=algorithm,
                    dateTime=utils.dateTime(),
                    runTime=round(toc-tic, 0),
                    isSuccess=isSuccess
                )

                totalImagesChecked += 1
                facesDetected += len(result.get_faces())
                totalRuntime += result.get_runTime()
                
                # Save new image file
                cv2.imwrite(offlineOutputPath + '/' + filename, result.get_img())

                result.setAny(
                    resultSaveLoc=offlineOutputPath,
                    algorithm=algorithm,
                    dateTime=utils.dateTime(),
                    runTime=round(toc-tic, 0),
                    isSuccess=isSuccess
                )
                
                if isTrained :
                    totalFalseDetections += result.get_falseDetections()
                    totalAccuracy += result.get_accuracy()
                
                result.set_img(f'{filename}')
                base = Path(workingFolder + '\\results')
                data = []
                jsonpath = base / ('offline.json')
                jsonpath.write_text(json.dumps(data))
                utils.appendJSON(offlineDataLocation, result)
        #print("Reached 6")
        if (totalImagesChecked < 1) :
            print("No images checked")
            return
        avgFaces = (facesDetected / totalImagesChecked)
        avgRuntime = (totalRuntime / totalImagesChecked)

        if isTrained :
            avgFalseDetections = (totalFalseDetections / totalImagesChecked)
            avgAccuracy = (totalAccuracy / totalImagesChecked)    
        else:
            avgFalseDetections = 'na'
            avgAccuracy = 'na'
        #print("Reached 7")
        callingScript.updateOfflineResults(totalRuntime,avgRuntime,facesDetected,avgFaces)
        #print("Reached 8")
        # Writing test result in latex format to txt file
        f = open(offlineLatexLocation, 'w+')
        table = [algorithm, str(totalRuntime), str(avgRuntime), str(facesDetected), str(avgAccuracy), str(avgFalseDetections)]
        
        
        tempStr = ''
        for data in table :
            tempStr += data + '&'

        # Trim last '&' and append double-backslash
        tempStr = tempStr[:-1] + r' \\'
        f.write(tempStr)
        
        f.close()

        print('Average Runtime: ' + str(avgRuntime))
        print('Faces Detected: ' + str(facesDetected))
        print('Average Accuracy: ' + str(avgAccuracy))
        print('Total False Detections: ' + str(totalFalseDetections))
        print('Marked images saved to ' + offlineOutputPath)
        print('JSON test results data saved to ' + offlineDataLocation)
        

def runOffline(callingScript, args):
    print('Running Offline Mode')
    print('...')
    thread1 = myThread(callingScript, args)
    thread1.start()
    print("Exiting main thread")
    

def delPreviousResults(offlineOutputPath, offlineDataLocation) :
    f = open(offlineDataLocation, 'w+')
    f.write('[]')
    f.close()

    for filename in os.listdir(offlineOutputPath) :
        os.remove(offlineOutputPath + '/' + filename)

def runTest(result, data, filename, workingFolder) :
    faces = result.get_faces()
    img = result.get_img()

    successCount = 0
    for (px, py) in data :
        found = False
        for (x,y,w,h) in faces :
            x1, y1 = x , y
            x2, y2 = x1+w, y1+h
            if (x1 < px and px < x2):
                if (y1 < py and py < y2):
                    found = True
                    successCount+=1
            
        if not found :
            result.set_img(cv2.rectangle(img, (px-100, py-100), (px+100, py+100),
                    (0, 0, 255), 2))
            
    falseDetections=len(faces) - successCount
    accuracy = successCount / len(data)

    result.setAny(
        accuracy=accuracy,
        falseDetections=falseDetections
    )
    
    # save image file if any false detections
    if falseDetections !=0 :
        cv2.imwrite(workingFolder + '/' + filename, result.get_img())

    ##TODO: Also save image file if accuracy not 1
    if successCount == len(data) :
        return True
    else :
        return False