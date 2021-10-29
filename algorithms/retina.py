from algorithms.testresults import TestResults
from retinaface import RetinaFace
import cv2
import config
import numpy as np
import utils


def getResult(location) :
    result = TestResults()
    img = cv2.cvtColor(cv2.imread(location), cv2.COLOR_BGR2RGB)
    
    resp = RetinaFace.detect_faces(location)

    faces = []
    confidences = []
    for face in resp :
        confidences.append(resp[face]['score'])
        single_face = []
        for num in resp[face]['facial_area'] :
            single_face.append(num.item())
            
        single_face[2] = single_face[2] - single_face[0]
        single_face[3] = single_face[3] - single_face[1]
        faces.append(single_face)
        
    result.set_confidence(confidences)
    result.set_isSuccess('na')
    with open(location, "rb") as fp:
        marked_img = utils.drawFaces(fp.read(), faces, result)
        result.set_img(marked_img) 

    return result


