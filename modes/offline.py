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
import os
import cv2

from tqdm import tqdm
from mtcnn_cv2 import MTCNN
from retinaface import RetinaFace


from algorithms import mtcnn
from algorithms import haar_cascade
from algorithms import retina

def runOffline(callingScript, args):
    print('Running Offline Mode')
    print('...')
    algorithm = args[0]
    dataset = args[1]  
    
    if args[2] == '':
        limit = 0
    else:
        limit = int(args[2])
    
    markName = args[3]  
  
    #NOTE (SEAN VONNEGUT): Was best to get the whole path from kivy so I did not use config.markingsLoc. Let me know if it is needed.
    path = dataset
    markPath = dataset + '/' + markName + '.json' #JSON file must be inside the dataset folder if mark name is included.

    isTrained = False

    if markName != "":
        isTrained = True
        data = utils.loadJSON(markPath)
        i = 0

    # if os.path.isfile(markPath) :
    #     data = utils.loadJSON(markPath)
    # else :
    #     data = []

    delPreviousResults()

    facesDetected = 0
    totalRuntime = 0
    totalImagesChecked = 0 #Counted instead of getting length of list since some files may have a invaild file type
    
    if isTrained :
        totalFalseDetections = 0
        totalAccuracy = 0
    else:
        totalFalseDetections = 'na'
        totalAccuracy = 'na'
    
    # Gets list paths to images in selected dataset
    images = os.listdir(path)
    
    # Shrink list to limit arg
    if limit != 0 : del images[limit:]

    totalNumberOfFiles = len(images)
    # Initialize algorithm
    if algorithm == 'mtcnn' :
        det = MTCNN()
    elif algorithm == 'haar' :
        det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    elif algorithm == 'retina' :
        model = RetinaFace.build_model()


    for filename in tqdm(images) :
        if (filename[-3:] == "png") | (filename[-3:] == "jpg"): #Accepted file types
          currentScanProgress = (totalImagesChecked+1) / totalNumberOfFiles
          callingScript.updateOfflineProgress(currentScanProgress, filename)

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
              isSuccess = runTest(result, marks, filename)
          else : 
              isSuccess = 'na'

          result.setAny(
              resultSaveLoc=config.offlineOutputPath,
              algorithm=algorithm,
              dateTime=utils.dateTime(),
              runTime=round(toc-tic, 0),
              isSuccess=isSuccess
          )

          totalImagesChecked += 1
          facesDetected += len(result.get_faces())
          totalRuntime += result.get_runTime()
          
          # Save new image file
          cv2.imwrite(config.offlineOutputPath + '/' + filename, result.get_img())

          result.setAny(
              resultSaveLoc=config.offlineOutputPath,
              algorithm=algorithm,
              dateTime=utils.dateTime(),
              runTime=round(toc-tic, 0),
              isSuccess=isSuccess
          )
        
          if isTrained :
            totalFalseDetections += result.get_falseDetections()
            totalAccuracy += result.get_accuracy()
          
          result.set_img(f'{filename}')
          utils.appendJSON(config.offlineDataLocation, result)
    
    avgFaces = (facesDetected / totalImagesChecked)
    avgRuntime = (totalRuntime / totalImagesChecked)

    if isTrained :
        avgFalseDetections = (totalFalseDetections / totalImagesChecked)
        avgAccuracy = (totalAccuracy / totalImagesChecked)    
    else:
        avgFalseDetections = 'na'
        avgAccuracy = 'na'
    
    callingScript.updateOfflineResults(totalRuntime,avgRuntime,facesDetected,avgFaces)

    # Writing test result in latex format to txt file
    f = open(config.offlineLatexLocation, 'w+')
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
    print('Marked images saved to ' + config.offlineOutputPath)
    print('JSON test results data saved to ' + config.offlineDataLocation)

def delPreviousResults() :
    f = open(config.offlineDataLocation, 'w+')
    f.write('[]')
    f.close()

    for filename in os.listdir(config.offlineOutputPath) :
        os.remove(config.offlineOutputPath + '/' + filename)

def runTest(result, data, filename) :
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
        cv2.imwrite(config.offlineOutputPath + '/' + filename, result.get_img())

    ##TODO: Also save image file if accuracy not 1
    if successCount == len(data) :
        return True
    else :
        return False