"""
Runs the MTCNN algorithm on given image.

Returns a TestResults object containing marked image and test data
"""

from mtcnn_cv2 import MTCNN
from algorithms.testresults import TestResults
import cv2
import config
import numpy as np


def getResult(location) :
    # initialize TestResults class that stores test results and can encode to json
    result = TestResults()
    # initialize imported mtcnn algorithm
    detector = MTCNN()
    # load selected image with opencv
    img = cv2.cvtColor(cv2.imread(location), cv2.COLOR_BGR2RGB)
    # use mtcnn to detect faces and store in a list
    data = detector.detect_faces(img)
    # set algorithm-dependent test values
    result.set_confidence(round(data[0]['confidence'], 5))
    result.set_isSuccess(len(data) > 0)
    # save the marked image to TestResults object
    with open(location, "rb") as fp:
        marked_img = drawFaces(fp.read(), data)
        result.set_img(marked_img)
    # return TestResult object to instant mode 
    return result


# draws detected face boxes on image
# if other algorithms use a similar method, move to utils
def drawFaces(img_data, results) :
    print(type(img_data))
    im = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
    for result in results:
        bounding_box = result['box']
        keypoints = result['keypoints']
        cv2.rectangle(image,
                        (bounding_box[0], bounding_box[1]),
                        (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                        (0, 155, 255),
                        2)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    is_success, im_buf_arr = cv2.imencode(".jpg", image) # TODO: Add support for other extentions (.png)
    return im_buf_arr

