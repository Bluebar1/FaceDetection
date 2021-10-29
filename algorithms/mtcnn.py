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


def getResult(location) :
    # initialize TestResults class that stores test results and can encode to json
    result = TestResults()
    # initialize imported mtcnn algorithm
    detector = MTCNN()
    # load selected image with opencv
    img = cv2.cvtColor(cv2.imread(location), cv2.COLOR_BGR2RGB)
    # use mtcnn to detect faces and store in a list
    data = detector.detect_faces(img)
    faces = []
    confidences = []
    for face in data :
        faces.append(face['box'])
        confidences.append(face['confidence'])

    # set algorithm-dependent test values
    # result.set_confidence(round(data[0]['confidence'], 5))
    result.set_confidence(confidences)
    result.set_isSuccess(len(data) > 0)
    # save the marked image to TestResults object
    with open(location, "rb") as fp:
        marked_img = utils.drawFaces(fp.read(), faces, result)
        result.set_img(marked_img)
    # return TestResult object to instant mode 
    return result


