"""
Allow uploading a photo, detect faces, and show the detected face in the photo

Arguments:
    Location of file to be tested
    Name of algorithm
"""

# import cv2
import config
import utils
import cv2
import os
import json
from PIL import Image
from algorithms import mtcnn
from algorithms import haar_cascade
from algorithms import retina
from pathlib import Path

def runInstant(callingScript, args):
    
    algorithm = args[0]
    location = args[1]
    workingFolder = args[2]
    instantDataLocation = workingFolder + config.instantDataLocation
    instantImageOutput = workingFolder + config.instantImageOutput
    #print("runInstnat success called")
    os.makedirs(workingFolder + '\\results\\', exist_ok=True)
    os.makedirs(workingFolder + '\\images\\output\\', exist_ok=True)

    # location = f'{config.inputPath}/{args[1]}'

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
    result.set_resultSaveLoc(instantImageOutput)
    result.set_algorithm(algorithm)
    result.set_dateTime(utils.dateTime())
    result.set_runTime(round(toc-tic, 0))

    # Save new image file
    # with open(instantImageOutput, "wb") as fp:
    #     fp.write(result.get_img())
    print('WRITTING IMAGE')
    cv2.imwrite(instantImageOutput, result.get_img())

    # Change image to string of location because json cannot encode image objects
    result.set_img(f'{location}')
    # append result to JSON file
    base = Path(workingFolder + '\\results')
    data = []
    jsonpath = base / ('instant.json')
    jsonpath.write_text(json.dumps(data))
    utils.appendJSON(instantDataLocation, result)
    
    print(f'JSON result appended to {instantDataLocation}')
    print(f'Marked images saved to {instantImageOutput}')

    callingScript.updateInstantResults(result.get_runTime(), len(result.get_faces()), result.get_resultSaveLoc())
    
    # Open image in new window
    #print('Opening image...')
    #im = Image.open(instantImageOutput)
    #im.show()

