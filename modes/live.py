"""
Allow live camera capture, detect faces in the live stream, and show the detected faces in the live camera feed.

Arguments:
    Name of algorithm to run
"""

import cv2
from algorithms import mtcnn
from mtcnn_cv2 import MTCNN
from retinaface import RetinaFace
import numpy as np
import utils
import config
import time
import os


def liveMTCNN() :
    print('Running live. Press Q to quit')
    detector = MTCNN()
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)

    prevFrameTime = 0
    newFrameTime = 0
    
    while(True):
        ret, frame = cap.read()

        frame = cv2.resize(frame, (600, 400))
        boxes = detector.detect_faces(frame)
        faces = []
        for box in boxes :
                faces.append(box['box'])
        
        utils.drawFaces(frame, faces)

        frame = cv2.putText(frame, 'Running MTCNN', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        newFrameTime = time.time()
        fps = str(int(1/(newFrameTime-prevFrameTime)))
        prevFrameTime = newFrameTime
        frame = cv2.putText(frame, 'FPS: ' + fps, (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        frame = cv2.putText(frame, 'Press q to quit', (20, 90), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,255), 1, cv2.LINE_AA)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def liveHaar() :
    print('Running live. Click on video window and press Q to quit')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)

    prevFrameTime = 0
    newFrameTime = 0

    while(True) :
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 400))
        faces = face_cascade.detectMultiScale(frame)
        utils.drawFaces(frame, faces)
        
        frame = cv2.putText(frame, 'Running Haar', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        newFrameTime = time.time()
        fps = str(int(1/(newFrameTime-prevFrameTime)))
        prevFrameTime = newFrameTime
        frame = cv2.putText(frame, 'FPS: ' + fps, (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        frame = cv2.putText(frame, 'Press q to quit', (20, 90), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,255), 1, cv2.LINE_AA)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def liveRetina(outputFolder) :
    
    model = RetinaFace.build_model()
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)
    print('Running live. Click on video window and press Q to quit')

    prevFrameTime = 0
    newFrameTime = 0
    os.makedirs(outputFolder + config.outputPath, exist_ok=True)
    while(True) :
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 400))
        cv2.imwrite(outputFolder + config.retinaTempSaveLocation, frame)
        resp = RetinaFace.detect_faces(outputFolder + config.retinaTempSaveLocation, model=model)
        if type(resp) is tuple :
            faces = []
        else :
            faces = []
            for face in resp :

                single_face = []
                for num in resp[face]['facial_area'] :
                    single_face.append(num.item())
            
                single_face[2] = single_face[2] - single_face[0]
                single_face[3] = single_face[3] - single_face[1]
                faces.append(single_face)

            
            utils.drawFaces(frame, faces)
        
        frame = cv2.putText(frame, 'Running RetinaFace', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        newFrameTime = time.time()
        fps = str(int(1/(newFrameTime-prevFrameTime)))
        prevFrameTime = newFrameTime
        frame = cv2.putText(frame, 'FPS: ' + fps, (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
        
        frame = cv2.putText(frame, 'Press q to quit', (20, 90), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,255), 1, cv2.LINE_AA)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def runLive(args, o) :
    algorithm = args
    outputFolder = o
    if algorithm == 'mtcnn' :
        liveMTCNN(outputFolder)
    elif algorithm == 'haar' :
        liveHaar(outputFolder)
    elif algorithm == 'retina' :
        liveRetina(outputFolder)