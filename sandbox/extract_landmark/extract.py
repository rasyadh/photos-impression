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
predictor = dlib.shape_predictor('../../project/face_landmark/shape_predictor_68_face_landmarks.dat')

DATASET_FILE_PATH = '../../project/static/image/dataset/jaffe/dataset_jaffe.json'
with open(DATASET_FILE_PATH) as f:
    data = json.load(f)
    f.close()

# load the input image, resize it, and convert it to grayscale
for index in data:
    for image in data[index]:
        image = cv2.imread('../../' + image['url'])
        image = imutils.resize(image, width=120)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        rects = detector(gray, 1)

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            feature = list()

            # loop over the face parts individually

            for(name, (i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                for(x,y) in shape[i:j]:
                    if name == "mouth":
                        cv2.circle(image, (x,y),1,(0,0,255), -1)
                        print ("Mulut : ")
                        print (x,y)
                        feature.append(x)
                        feature.append(y)
                    elif name == "left_eyebrow":
                        cv2.circle(image, (x,y),1,(0,0,255), -1)
                        print ("Alis kiri : ")
                        print (x,y)
                        feature.append(x)
                        feature.append(y)
                    elif name == "right_eyebrow":
                        cv2.circle(image, (x,y),1,(0,0,255), -1)
                        print ("Alis Kanan : ")
                        print (x,y)
                        feature.append(x)
                        feature.append(y)
                    elif name == "left_eye":
                        cv2.circle(image, (x,y),1,(0,0,255), -1)
                        print ("Mata kiri : ")
                        print (x,y)
                        feature.append(x)
                        feature.append(y)
                    elif name == "right_eye":
                        cv2.circle(image, (x,y),1,(0,0,255), -1)
                        print ("Mata kanan : ")
                        print (x,y)
                        feature.append(x)
                        feature.append(y)
        
        print(len(feature))
        print(feature)

        newmaks_x = 1
        newmaks_y = 1
        newmin_x = 0
        newmin_y = 0
        minimal_y = 1000
        minimal_x = 1000
        maks_x = 0
        maks_y = 0

        for b in range(len(feature)):
            if (b % 2 == 0):
                if (feature[b] < minimal_x):
                    minimal_x = float(feature[b])
                if (feature[b] > maks_x):
                    maks_x = float(feature[b])
            else:
                if (feature[b] < minimal_y):
                    minimal_y = float(feature[b])
                if (feature[b] > maks_y):
                    maks_y = float(feature[b])

        print(minimal_x)
        print(minimal_y)
        print(maks_x)
        print(maks_y)

        for c in range(len(feature)):
            if (c%2 == 0):
                newdata = (float(feature[c])-minimal_x) * (newmaks_x - newmin_x) / (maks_x - minimal_x) + newmin_x
                feature[c] = newdata
            else:
                newdata = (float(feature[c])-minimal_y) * (newmaks_y - newmin_y) / (maks_y - minimal_y) + newmin_y
                feature[c] = newdata
                
        print(type(feature))

        with open('fitur.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(feature)