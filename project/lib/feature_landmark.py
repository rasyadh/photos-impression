import os
import json
from imutils import (
    face_utils,
    resize
)
import numpy as np
import dlib
import cv2
from project.lib.normalization import Normalization

class FeatureLandmark:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        path_predictor = 'project/face_landmark/shape_predictor_68_face_landmarks.dat'
        self.predictor = dlib.shape_predictor(path_predictor)

    def get_face_landmark(self, FILE_PATH, size=120):
        # read image data
        image = cv2.imread(FILE_PATH)
        image = resize(image, width=size)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        rects = self.detector(gray, 1)

        feature = []

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # loop over the face parts individually
            for (name, (i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                for (x,y) in shape[i:j]:
                    if name == "mouth":
                        feature.append(x)
                        feature.append(y)
                    elif name == "left_eyebrow":
                        feature.append(x)
                        feature.append(y)
                    elif name == "right_eyebrow":
                        feature.append(x)
                        feature.append(y)
                    elif name == "left_eye":
                        feature.append(x)
                        feature.append(y)
                    elif name == "right_eye":
                        feature.append(x)
                        feature.append(y)
        
        norm = Normalization()
        feature = norm.normalize(feature)

        return feature

    def get_feature(self, DATASET_PATH, FILE_PATH, size, i_dataset):
        with open(FILE_PATH) as dataset:
            i_data = json.load(dataset)
            dataset.close()

        feature, target, classes = [], [], []
        for index in i_data:
            for image in i_data[index]:
                face_feature = self.get_face_landmark(image['url'], size)

                feature.append(face_feature)
                target.append(image['id_expression'])

            classes.append(index)

        dataset = {
            'data': feature,
            'target': target,
            'classes': classes,
            'shape': size
        }

        with open(DATASET_PATH + 'feature_landmark_' + i_dataset + '_dataset.json', 'w') as outfile:
            json.dump(dataset, outfile)
            outfile.close()

    def read_dataset(self, DATASET_PATH, dataset):
        if dataset == 'jaffe':
            FILE_PATH = DATASET_PATH + 'dataset_jaffe.json'
        else:
            FILE_PATH = DATASET_PATH + 'dataset_indonesia.json'
        result, data = {}, []

        try:
            for dirname, dirnames, filenames in os.walk(DATASET_PATH):
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    for filename in os.listdir(subject_path):
                        if subdirname == 'NE':
                            id_expression = 0
                        elif subdirname == 'HA':
                            id_expression = 1
                        elif subdirname == 'SA':
                            id_expression = 2
                        elif subdirname == 'SU':
                            id_expression = 3

                        temp = {}
                        temp = {
                            'name': filename,
                            'url': 'project/static/image/dataset/' + dataset + '/' + subdirname + '/' + filename,
                            'id_expression': id_expression
                        }

                        data.append(temp)
                        
                    result[subdirname] = data
                    data = []
        except Exception as e:
            print(e)

        with open(FILE_PATH, 'w') as outfile:
            json.dump(result, outfile)
            outfile.close()

        self.get_feature(DATASET_PATH, FILE_PATH, 120, dataset)