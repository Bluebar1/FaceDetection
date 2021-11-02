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
from algorithms import mtcnn
from algorithms import haar_cascade
from algorithms import retina

def runOffline(args):
    print('Running Offline Mode')
    print('...')
    folder = config.inputPath
    algorithm = args[2]

    delPreviousResults()

    facesDetected = 0
    confidence = 0
    totalRuntime = 0
    totalImages = len(os.listdir(folder))

    for filename in os.listdir(folder) :
        tic = utils.currentTime()
        
        if algorithm == 'mtcnn' :
            result = mtcnn.getResult(folder + '/' + filename)
        elif algorithm == 'haar' :
            result = haar_cascade.getResult(folder + '/' + filename)
        elif algorithm == 'retina' :
            result = retina.getResult(folder + '/' + filename)
            
        toc = utils.currentTime()
        result.set_resultSaveLoc(config.offlineOutputPath)
        result.set_algorithm(algorithm)
        result.set_dateTime(utils.dateTime())
        result.set_runTime(round(toc-tic, 0))

        facesDetected += len(result.get_faces())
        totalRuntime += result.get_runTime()

        if algorithm != 'haar' :

            for conf in result.get_confidence() :
                confidence += conf
                # facesDetected += 1

        




        # Save new image file
        with open(config.offlineOutputPath + '/' + filename, "wb") as fp:
            fp.write(result.get_img())

        result.set_img(f'{filename}')
        utils.appendJSON(config.offlineDataLocation, result)

    

    avgConfidence = round(confidence / facesDetected, 5)
    avgFaces = (facesDetected / totalImages)
    avgRuntime = (totalRuntime / totalImages)

    if algorithm == 'haar' :
        avgConfidence = 'na'

    f = open(config.offlineLatexLocation, 'w+')
    # latexString = algorithm + '&' + totalRuntime + '&' + avgRuntime + '&' + 
    table = [algorithm, str(totalRuntime), str(avgRuntime), str(facesDetected), str(avgFaces), str(avgConfidence)]
    tempStr = ''
    for data in table :
        tempStr += data + '&'
        print(tempStr)

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

    



    
