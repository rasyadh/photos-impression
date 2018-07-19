# USAGE
# python detect_face_parts.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg 

# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import csv
import math
import json

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('../../../project/face_landmark/shape_predictor_68_face_landmarks.dat')
capture = cv2.VideoCapture(0)

while True:
    success, image = capture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        for(name, (i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            for(x,y) in shape[i:j]:
                if name == "mouth":
                    cv2.circle(image, (x,y),3,(0,255,0), -1)
                elif name == "left_eyebrow":
                    cv2.circle(image, (x,y),3,(0,255,0), -1)
                elif name == "right_eyebrow":
                    cv2.circle(image, (x,y),3,(0,255,0), -1)
                elif name == "left_eye":
                    cv2.circle(image, (x,y),3,(0,255,0), -1)
                elif name == "right_eye":
                    cv2.circle(image, (x,y),3,(0,255,0), -1)

    cv2.imshow('webcam', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()