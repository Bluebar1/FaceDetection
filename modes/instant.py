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
from algorithms import haar_cascade
from algorithms import retina

def runInstant(args):
    
    algorithm = args[0]
    location = f'{config.inputPath}/{args[1]}'

    print(f'Running instant mode \n Algorithm: {algorithm} \n File: {location} \n ...')
    
    # start timer
    tic = utils.currentTime()

    if algorithm == 'mtcnn' :
        result = mtcnn.getResult(location)
    elif algorithm == 'haar' :
        result = haar_cascade.getResult(location)
    elif algorithm == 'retina' :
        result = retina.getResult(location)
        
        
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
    print(f'JSON result appended to {config.instantDataLocation}')
    print(f'Marked images saved to {config.instantImageOutput}')
    print('Opening image...')
    im = Image.open(config.instantImageOutput)
    im.show()
