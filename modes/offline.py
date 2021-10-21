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

def runOffline(args):
    print('runOffline')
    folder = config.inputPath
    algorithm = 'mtcnn'

    delPreviousResults()

    for filename in os.listdir(folder) :
        tic = utils.currentTime()
        result = mtcnn.getResult(folder + '/' + filename)
        toc = utils.currentTime()
        result.set_resultSaveLoc(config.offlineOutputPath)
        result.set_algorithm(algorithm)
        result.set_dateTime(utils.dateTime())
        result.set_runTime(round(toc-tic, 0))

        # Save new image file
        with open(config.offlineOutputPath + '/' + filename, "wb") as fp:
            fp.write(result.get_img())

        result.set_img(f'{filename}')
        utils.appendJSON(config.offlineDataLocation, result)

def delPreviousResults() :
    f = open(config.offlineDataLocation, 'w+')
    f.write('[]')
    f.close()

    for filename in os.listdir(config.offlineOutputPath) :
        os.remove(config.offlineOutputPath + '/' + filename)

    



    
