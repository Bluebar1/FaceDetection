# FaceDetection
ICSI499 Capstone Project  

Commands to run:  

git clone https://github.com/Bluebar1/FaceDetection.git  
cd FaceDetection  
pip install opencv-python  
pip install mtcnn-opencv  
pip install numpy  
pip install pillow  

To run this program simply type the command  
python main.py  

Our goal is to use multiple face detection algorithms to analyze how masks affect their ability to detect faces. Each of these algorithm can be used in the modes:  

Instant:  
<space><space><space>	Parameters: Algorithm, image file  
<space><space><space>	-Starts a timer  
<space><space><space>-Create TestResults instance for storing results  
<space><space><space>	-Get results for given algorithm and image  
<space><space><space>-Save new marked image file to data/images/output/instant_result.jpg  
<space><space><space>-Append JSON result to data/results/instant.json  
<space><space><space>-Open marked image in new window  

Offline:  
<space><space><space>Parameters: Algorithm, dataset folder, limit, isTrained  
<space><space><space>-If user trained the dataset, load correct coordinates json file  
<space><space><space>-Delete any previous image and json results to limit memory usage  
<space><space><space>-Create instance of given algorithm and use it for all images in the given dataset folder within the given limit  
<space><space><space>-Save each marked image to data/images/output/offline/ folder  
<space><space><space>-Calculate average confidence, average faces detected, and average runTime  
<space><space><space>-If user trained the dataset, calculate accuracy and # of false detections  
<space><space><space>-Append each JSON result to data/results/offline.json  
<space><space><space>-Write results in latex format to data/results/latex.txt to be easily pasted into our research document  
	

Live:  
<space><space><space>	Parameter: Algorithm  
<space><space><space>-Initialize given algorithm  
<space><space><space>-Establish connection to webcam using OpenCV  
<space><space><space>-Start while(True) loop that will break when ‘q’ key is pressed  
<space><space><space>-For each iteration, detect faces in current frame of video feed  
<space><space><space>-Draw and display marked image  
 
Algorithm Overview:  

MTCNN: (mtcnn_cv2)  
<space><space><space>	-detector = MTCNN()  
<space><space><space>	-detector.detect_faces(image)  
<space><space><space>	-This returns a list of dictionary objects and can be accessed using  
<space><space><space>	-data[face][‘box’] for (x,y,w,h) coordinates  
<space><space><space>	-data[face][‘confidence’] for the confidence of each  

Haar Cascade: (OpenCV)  
<space><space><space>	-detector = cv2.CascadeClassifier(cv2.data.haarcascades+  
<space><space><space>"haarcascade_frontalface_default.xml")  
<space><space><space>	-detector.detectMultiScale(image)  
<space><space><space>	-This returns a numpy.ndarray object that can be converted to a list using:  
<space><space><space>	-face_data = faces.tolist()  
<space><space><space>	-Does not return confidence levels  

Retina: (RetinaFace)  
<space><space><space>	-model = RetinaFace.build_model()  
<space><space><space>	-RetinaFace.detect_faces(location, model=model)  
<space><space><space>	-This will return a dictionary object and can be accessed using:  
<space><space><space>	-data[face][‘facial_area’] for boxes  
<space><space><space>	-data[face][‘score’] for confidence level  

How coordinates work:  

<space><space><space>-Box coordinates of detected faces are stored in a (x, y, width, height) format  
<space><space><space>-In offline mode using the correct (x,y) points, each point will be compared to the detected faces to see if the point is within any of the detected boxes  
<space><space><space>-Accuracy for each image will be calculated: SuccessCount / len(correctPoints)  
<space><space><space>-False Detections will be calculated: len(detectedFaces) - successCount  


Inputting correct face coordinates:  
<space><space><space>	Run marker.py file  
<space><space><space>	Parameters: Dataset folder, limit  
<space><space><space>	-For each image in the given dataset folder within the given limit:  
<space><space><space>		-Open image in new window  
<space><space><space>		-Left click on faces to mark them  
<space><space><space>		-Right click image to reset (undo misclick)  
<space><space><space>		-Press ‘n’ to append points to JSON file and go to next image  


  
