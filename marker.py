

import cv2
import config
import os
import utils
import json
from tqdm import tqdm

  



def click_event(event, x, y, flags, params):
    global img
    global faces
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(img, (x-4, y-4), (x + 4, y + 4),
             (0, 255, 0), 2)
        cv2.imshow('image', img)
        faces.append([x,y])
        
 
    # checking for right mouse clicks    
    elif event==cv2.EVENT_RBUTTONDOWN:
        img = clone.copy()
        cv2.imshow('image', img)
        faces.clear()
        
        
 

# driver function
if __name__=="__main__":
    

    dataset = input('Enter the name of the folder found in your data/images/input directory. Examples test|ffhq \n : ')
    print('Entering marking mode for dataset: ' + dataset)
    imagesPath = config.inputPath + '/' + dataset + '/'
    print(imagesPath)
    # Check if dataset folder exists in data/images/input/
    jsonpath = config.markingsLoc + dataset + '_markings.json'
    if os.path.isdir(imagesPath) != True:
        print('Directory does not exist. Exiting...')
        quit()
    if not os.path.exists(os.path.dirname(jsonpath)):
        try:
            os.makedirs(os.path.dirname(jsonpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != EOFError.EEXIST:
                raise
    
    f = open(jsonpath, 'w+')
    f.write('[]')
    f.close()
    
    faces = []
    
    
    

    images = os.listdir(imagesPath)

    
    

    for im in tqdm(images) :
        data = utils.loadJSON(jsonpath)
        faces.clear()
        img = cv2.imread(imagesPath + im, 1)
        clone = img.copy()
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', click_event)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q') :
            quit()
        elif key == ord('n') :
            data.append(faces)
            with open(jsonpath, 'w') as file:
                json.dump(data, file)
    
    # close the window
    cv2.destroyAllWindows()





