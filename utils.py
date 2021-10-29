import time
from datetime import datetime
import json
import config
import cv2
import numpy as np


# Helper functions

def currentTime() :
    return time.time() * 1000

def dateTime() :
    return datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")


def appendJSON(filePath, jsonData) :
    with open(filePath, 'r') as file:
        data = json.load(file)

    # decode and append data
    dict_obj = json.loads(jsonData.toJSON())
    data.append(dict_obj)
    
    # write to file
    with open(filePath, 'w') as file:
        json.dump(data, file)



def drawFaces(img_data, faces, testResult) :
    im = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
    for (x,y,w,h) in faces:
        image = cv2.rectangle(image, (x, y), (x + w, y + h),
            (0, 255, 0), 2)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    is_success, im_buf_arr = cv2.imencode(".jpg", image) # TODO: Add support for other extentions (.png)
    testResult.set_faces(faces)
    return im_buf_arr