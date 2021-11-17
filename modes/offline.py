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

def runOffline(args):
    print('Running Offline Mode')
    print('...')
    algorithm = args[0]
    dataset = args[1]
    limit = int(args[2])

    
    
    path = config.inputPath + '/' + dataset
    markPath = config.markingsLoc + dataset + '_markings.json'

    isTrained = False
    if args[3] == 'y' :
        isTrained = True
        data = utils.loadJSON(markPath)
        i = 0


    # if os.path.isfile(markPath) :
    #     data = utils.loadJSON(markPath)
    # else :
    #     data = []

    delPreviousResults()

    facesDetected = 0
    confidence = 0
    totalRuntime = 0
    
    # Gets list paths to images in selected dataset
    images = os.listdir(path)
    
    # Shrink list to limit arg
    if limit != 0 : del images[limit:]

    if algorithm == 'mtcnn' :
        det = MTCNN()
    elif algorithm == 'haar' :
        det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
    elif algorithm == 'retina' :
        model = RetinaFace.build_model()

    for filename in tqdm(images) :
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
            isSuccess = runTest(result, marks)
        else : 
            isSuccess = 'na'

        result.setAny(
            resultSaveLoc=config.offlineOutputPath,
            algorithm=algorithm,
            dateTime=utils.dateTime(),
            runTime=round(toc-tic, 0),
            isSuccess=isSuccess
        )
        

        facesDetected += len(result.get_faces())
        totalRuntime += result.get_runTime()

        if algorithm != 'haar' :

            for conf in result.get_confidence() :
                confidence += conf

        # Save new image file
        tic = utils.currentTime()
        cv2.imwrite(config.offlineOutputPath + '/' + filename, result.get_img())

        result.set_img(f'{filename}')
        utils.appendJSON(config.offlineDataLocation, result)

        
    
    
    totalImages = len(images)
    avgConfidence = round(confidence / facesDetected, 5)
    avgFaces = (facesDetected / totalImages)
    avgRuntime = (totalRuntime / totalImages)

    if algorithm == 'haar' :
        avgConfidence = 'na'


    # Writing test result in latex format to txt file
    f = open(config.offlineLatexLocation, 'w+')
    table = [algorithm, str(totalRuntime), str(avgRuntime), str(facesDetected), str(avgFaces), str(avgConfidence)]
    tempStr = ''
    for data in table :
        tempStr += data + '&'

    # Trim last '&' and append double-backslash
    tempStr = tempStr[:-1] + r' \\'
    f.write(tempStr)
    
    f.close()

    print('Marked images saved to ' + config.offlineOutputPath)
    print('JSON test results data saved to ' + config.offlineDataLocation)

def delPreviousResults() :
    f = open(config.offlineDataLocation, 'w+')
    f.write('[]')
    f.close()

    for filename in os.listdir(config.offlineOutputPath) :
        os.remove(config.offlineOutputPath + '/' + filename)


def runTest(result, data) :


    faces = result.get_faces()
    img = result.get_img()

    successCount = 0
    dataLength = len(data)

    
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
            
    
    result.setAny(
        accuracy=successCount / len(data),
        falseDetections=len(faces) - successCount
    )
    

    if successCount == len(data) :
        return True
    else :
        return False

    



