from algorithms.testresults import TestResults
from retinaface import RetinaFace
import cv2
import config
import numpy as np
import utils
import os
import tensorflow as tf


def getResult(location, model=None) :
    result = TestResults()
    
    if model is None :
        model = RetinaFace.build_model()
    
    resp = RetinaFace.detect_faces(location, model=model)

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
    result.set_faces(faces)

    marked_img = utils.drawFaces(cv2.imread(location), faces)
    result.set_img(marked_img)
    return result


