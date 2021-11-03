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

This demo program uses a MTCNN/Haars-Cascade/Retina facial detection algorithms across 3 different modes: 
Instant, Offline, and Live  

In Instant, a single photo in the input folder is ran through the detection algorithm and it saves JSON of test results  
and the marked image in the output program folder. The JSON data looks like this:    
{  
    "img": "data/images/input/test1.jpg",  
    "resultSaveLoc": "data/images/output/instant_result.jpg",  
    "algorithm": "mtcnn",  
    "dateTime": "10/28/2021, 11:32:27",  
    "runTime": 133.0,  
    "isSuccess": true,  
    "faces": [  
      [533, 35, 139, 173],  
      [454, 113, 90, 113],  
      [33, 103, 105, 133],  
      [265, 51, 65, 81],  
      [150, 7, 73, 95],  
      [370, 71, 58, 87]  
    ],  
    "confidence": [  
      0.9999963045120239,  
      0.9999741315841675,  
      0.9999641180038452,  
      0.9999223947525024,  
      0.9999125003814697,  
      0.9996563196182251  
    ]  
}  


In Offline, a folder containing many images is ran through the detection algorithm. The test results:  
Will be saved in JSON format to the data/results/offline.json file  
The marked images will be saved in the data/images/output/ directory.  
The latex formatted result will be saved to data/results/latex.txt  

In live, the program will open a live video feed from your computers camera and each frame will check for faces and draw the boxes if found.

  
