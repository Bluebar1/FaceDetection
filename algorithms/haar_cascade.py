from algorithms.testresults import TestResults
import cv2
import config
import numpy as np
import utils

def getResult(location, det=None) :
    result = TestResults()
    img = cv2.imread(location)

    if det is None :
        det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = det.detectMultiScale(img)

    if type(faces) is tuple : 
        face_data = []
    else : 
        face_data = faces.tolist()

    result.setAny(
        confidence='na',
        isSuccess='na',
        faces = face_data
    )

    marked_img = utils.drawFaces(img, face_data)
    result.set_img(marked_img)
    return result


