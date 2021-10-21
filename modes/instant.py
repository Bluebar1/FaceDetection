"""
Allow uploading a photo, detect faces, and show the detected face in the photo

Arguments:
    Location of file to be tested
    Name of algorithm
"""

# import cv2
import config
import utils
from PIL import Image
from algorithms import mtcnn

def runInstant(args):
    location = f"{config.inputPath}/{args[2]}"
    algorithm = args[3]
    # start timer
    tic = utils.currentTime()

    if algorithm == 'mtcnn' :
        result = mtcnn.getResult(location)
    else :
        print('Algorithm not supported')
        quit()

    # end timer
    toc = utils.currentTime()
    # finish loading result data
    result.set_resultSaveLoc(config.instantImageOutput)
    result.set_algorithm(algorithm)
    result.set_dateTime(utils.dateTime())
    result.set_runTime(round(toc-tic, 0))

    # Save new image file
    with open(config.instantImageOutput, "wb") as fp:
        fp.write(result.get_img())

    # Change image to string of location because json cannot encode image objects
    result.set_img(f'{location}')
    # append result to JSON file
    
    utils.appendJSON(config.instantDataLocation, result)
    # Open image in new window
    im = Image.open(config.instantImageOutput)
    im.show()
