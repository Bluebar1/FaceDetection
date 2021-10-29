from algorithms.testresults import TestResults
import cv2
import config
import numpy as np
import utils

def getResult(location) :
    result = TestResults()
    img = cv2.cvtColor(cv2.imread(location), cv2.COLOR_BGR2RGB)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(img)
    face_data = faces.tolist()
    
    result.set_confidence('na')
    result.set_isSuccess('na')
    with open(location, "rb") as fp:
        marked_img = utils.drawFaces(fp.read(), face_data, result)
        result.set_img(marked_img) 
    return result


