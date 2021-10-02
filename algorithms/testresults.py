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
        self.confidence = float
        self.isSuccess = bool

    
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
    
    def get_confidence(self) :
        return self.confidence

    def get_isSuccess(self) :
        return self.isSuccess


    # Setters 

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

    def set_confidence(self, confidence) :
        self.confidence = confidence

    def set_isSuccess(self, isSuccess) :
        self.isSuccess = isSuccess


    