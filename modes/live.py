"""
Allow live camera capture, detect faces in the live stream, and show the detected faces in the live camera feed.

Arguments:
    Name of algorithm to run
"""

import cv2
from algorithms import mtcnn
from mtcnn_cv2 import MTCNN
import numpy as np
import config


def runLive(args) :
    
    detector = MTCNN()
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)

    while(True):
        ret, frame = cap.read()

        frame = cv2.resize(frame, (600, 400))
        boxes = detector.detect_faces(frame)
        if boxes:
 
            box = boxes[0]['box']
            conf = boxes[0]['confidence']
            x, y, w, h = box[0], box[1], box[2], box[3]
    
            if conf > 0.1:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    

