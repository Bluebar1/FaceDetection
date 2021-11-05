"""
Runs the MTCNN algorithm on given image.

Returns a TestResults object containing marked image and test data
"""

from mtcnn_cv2 import MTCNN
from algorithms.testresults import TestResults
import cv2
import config
import numpy as np
import utils


def getResult(location, det=None) :
    # initialize TestResults class that stores test results and can encode to json
    if det is None :
        det = MTCNN()

    result = TestResults()
    
    # load selected image with opencv
    img = cv2.imread(location)
    
    data = det.detect_faces(img)
    faces = []
    confidences = []
    for face in data :
        faces.append(face['box'])
        confidences.append(face['confidence'])

    
    result.set_confidence(confidences)
    result.set_isSuccess(len(data) > 0)
    result.set_faces(faces)
    marked_img = utils.drawFaces(img, faces)
    result.set_img(marked_img)
    return result


