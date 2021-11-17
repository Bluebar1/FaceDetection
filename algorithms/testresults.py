"""
Created NB 10/1/2021

Object to store results of tests.

img is initialized as type bytes to save marked image, 
but is changed to String before JSON encoding

"""

import json

class TestResults:

    def __init__(self) :
        self.img = bytes
        self.resultSaveLoc = ""
        self.algorithm = ""
        self.dateTime = ""
        self.runTime = float
        self.isSuccess = bool
        self.accuracy = 'na'
        self.falseDetections = 'na'
        self.faces = []
        self.confidence = []
        
        
    def toJSON(self) :
        # Encodes to JSON string using dictionary
        return json.dumps(self, default=lambda o: o.__dict__) 
        

    # Getters

    def get_img(self) :
        return self.img

    def get_resultSaveLoc(self) :
        return self.resultSaveLoc

    def get_algorithm(self) :
        return self.algorithm

    def get_dateTime(self) :
        return self.dateTime

    def get_runTime(self) :
        return self.runTime 

    def get_isSuccess(self) :
        return self.isSuccess

    def get_accuracy(self) :
        return self.accuracy

    def get_falseDetections(self) :
        return self.falseDetections

    def get_faces(self) :
        return self.faces

    def get_confidence(self) :
        return self.confidence


    # Setters 

    def setAny(self, img=None, resultSaveLoc=None, algorithm=None, dateTime=None, runTime=None, isSuccess=None, accuracy=None, falseDetections=None, faces=None, confidence=None) :
        # img causes error
        if resultSaveLoc != None : self.resultSaveLoc = resultSaveLoc
        if algorithm != None : self.algorithm = algorithm
        if dateTime != None : self.dateTime = dateTime
        if runTime != None : self.runTime = runTime
        if isSuccess != None : self.isSuccess = isSuccess
        if accuracy != None : self.accuracy = accuracy
        if falseDetections != None : self.falseDetections = falseDetections
        if faces != None : self.faces = faces
        if confidence != None : self.confidence = confidence

        

    def set_img(self, img) :
        self.img = img

    def set_resultSaveLoc(self, resultSaveLoc) :
        self.resultSaveLoc = resultSaveLoc

    def set_algorithm(self, algorithm) :
        self.algorithm = algorithm

    def set_dateTime(self, dateTime) :
        self.dateTime = dateTime

    def set_runTime(self, runTime) :
        self.runTime = runTime

    def set_isSuccess(self, isSuccess) :
        self.isSuccess = isSuccess

    def set_accuracy(self, accuracy) :
        self.accuracy = accuracy

    def set_falseDetections(self, falseDetections) :
        self.falseDetections = falseDetections

    def set_faces(self, faces) :
        self.faces = faces

    def set_confidence(self, confidence) :
        self.confidence = confidence
    