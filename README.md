# FaceDetection
ICSI499 Capstone Project  
 
## First Time Setup
Make sure python version <= 3.9  
cd into FaceDetection directory in windows command prompt  
> python -m pip install --upgrade pip setuptools virtualenv  
> python -m virtualenv virt  
> virt/Scripts/activate  
> python -m pip install kivy[base] kivy_examples  
> pip install -r requirements.txt  
> python new_kiv.py  

## Every time:
> source virt/Scripts/activate  
> python new_kiv.py    


# Project Overview
Our goal is to use multiple face detection algorithms to analyze how masks affect their ability to detect faces. Each of these algorithm can be used in the modes:  

## Instant:  
Parameters: Algorithm, image file  
-Starts a timer  
-Create TestResults instance for storing results  
-Get results for given algorithm and image  
-Save new marked image file to data/images/output/instant_result.jpg  
-Append JSON result to data/results/instant.json  
-Open marked image in new window  

## Offline:  
Parameters: Algorithm, dataset folder, limit, isTrained  
-If user trained the dataset, load correct coordinates json file  
-Delete any previous image and json results to limit memory usage  
-Create instance of given algorithm and use it for all images in the given dataset folder within the given limit  
-Save each marked image to data/images/output/offline/ folder  
-Calculate average confidence, average faces detected, and average runTime  
-If user trained the dataset, calculate accuracy and # of false detections  
-Append each JSON result to data/results/offline.json  
-Write results in latex format to data/results/latex.txt to be easily pasted into our research document  
	

## Live:  
Parameter: Algorithm  
-Initialize given algorithm  
-Establish connection to webcam using OpenCV  
-Start while(True) loop that will break when ‘q’ key is pressed  
-For each iteration, detect faces in current frame of video feed  
-Draw and display marked image  
 
# Algorithm Overview:  

## MTCNN: (mtcnn_cv2)  
-detector = MTCNN()  
-detector.detect_faces(image)  
-This returns a list of dictionary objects and can be accessed using  
-data[face][‘box’] for (x,y,w,h) coordinates  
-data[face][‘confidence’] for the confidence of each  

## Haar Cascade: (OpenCV)  
-detector = cv2.CascadeClassifier(cv2.data.haarcascades+  
"haarcascade_frontalface_default.xml")  
-detector.detectMultiScale(image)  
-This returns a numpy.ndarray object that can be converted to a list using:  
-face_data = faces.tolist()  
-Does not return confidence levels  

## Retina: (RetinaFace)  
-model = RetinaFace.build_model()  
-RetinaFace.detect_faces(location, model=model)  
-This will return a dictionary object and can be accessed using:  
-data[face][‘facial_area’] for boxes  
-data[face][‘score’] for confidence level  

## How coordinates work:  

-Box coordinates of detected faces are stored in a (x, y, width, height) format  
-In offline mode using the correct (x,y) points, each point will be compared to the detected faces to see if the point is within any of the detected boxes  
-Accuracy for each image will be calculated: SuccessCount / len(correctPoints)  
-False Detections will be calculated: len(detectedFaces) - successCount  


## Inputting correct face coordinates:  
Run marker.py file  
Parameters: Dataset folder, limit  
-For each image in the given dataset folder within the given limit:  
-Open image in new window  
-Left click on faces to mark them  
-Right click image to reset (undo misclick)  
-Press ‘n’ to append points to JSON file and go to next image  


  
