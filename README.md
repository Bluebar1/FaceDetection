# FaceDetection
ICSI499 Capstone Project  

Commands to run:  

git clone https://github.com/Bluebar1/FaceDetection.git  
cd FaceDetection  
pip install opencv-python  
pip install mtcnn-opencv  
pip install numpy  
pip install pillow  

python main.py instant test1.jpg mtcnn  
python main.py offline  
python main.py live  

This demo program uses a pretrained MTCNN facial detection algorithm across 3 different modes: 
Instant, Offline, and Live  

In Instant, a single photo in the input folder is ran through the detection algorithm and it saves JSON of test results  
and the marked image in the output program folder. The JSON data currently includes file name, file location, algorithm used,  
date/time, run-time in milliseconds, confidence, and a isSuccess boolean. We will also be storing the coordinates of multiple  
faces detected. Then, the marked image will open in a new window.

In Offline, a folder containing many images is ran through the detection algorithm. Similarly to instant mode, the test results  
will be saved in JSON format and the marked images will be saved in the data/images/output directory.

In live, the program will open a live video feed from your computers camera and each frame will check for faces and draw the boxes if found.

  
