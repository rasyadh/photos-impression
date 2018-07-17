import os
import json
import cv2
import numpy as np

class FeatureDataset:
    def _init_(self):
        return

    def get_faces(self, FILE_PATH, size=None):
        classifier = 'project/cascade/haarcascade_frontalface_default.xml'
        face = None

        # read image data
        image = cv2.imread(FILE_PATH, 0)
        # set cascade classifier 
        face_cascade = cv2.CascadeClassifier(classifier)
        # detect faces in image
        faces = face_cascade.detectMultiScale(
            image,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # get face area only
        for (x, y, w, h) in faces:
            # default face dimension 182x182
            face = image[y : (y + h), x : (x + w)]

            # resize image
            if (size is not None):
                face = cv2.resize(face, (size, size))

        return face

    def get_feature(self, DATASET_PATH, FILE_PATH, size, i_dataset):
        with open(FILE_PATH) as dataset:
            i_data = json.load(dataset)
            dataset.close()

        feature, target, classes = [], [], []
        for index in i_data:
            for image in i_data[index]:
                print(image)
                face = None
                face = self.get_faces(image['url'], size)
                face = face.flatten()

                feature.append(face.tolist())
                target.append(image['id_expression'])

            classes.append(index)

        dataset = {
            'data': feature,
            'target': target,
            'classes': classes,
            'shape': size
        }

        with open(DATASET_PATH + 'feature_' + i_dataset + '_dataset.json', 'w') as outfile:
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