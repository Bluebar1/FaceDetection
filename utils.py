import time
from datetime import datetime
import json
import config

# Helper functions

def currentTime() :
    return time.time() * 1000

def dateTime() :
    return datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")

def appendJSON(filePath, jsonData) :
    with open(filePath, 'r') as file:
        data = json.load(file)

    # decode and append data
    dict_obj = json.loads(jsonData.toJSON())
    data.append(dict_obj)
    
    # write to file
    with open(filePath, 'w') as file:
        json.dump(data, file)