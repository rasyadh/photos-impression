import cv2
import numpy as np
import json
from utils import Utils

size = 100
DATASET_FILE_PATH = 'jaffe\dataset_jaffe.json'
util = Utils('cascade\haarcascade_frontalface_default.xml')

with open(DATASET_FILE_PATH) as dataset:
    data = json.load(dataset)
    dataset.close()

feature, target, classes = [], [], []
for index in data:
    for photo in data[index]:        
        face = util.read_images(photo['url'], size)
        face = face.flatten()
        feature.append(face.tolist())
        target.append(index)
        face = None
    classes.append(index)

print(type(feature), type(target), type(classes))
dataset = {
    'data': feature,
    'target': target,
    'classes': classes
}

with open('feature_dataset.json', 'w') as outfile:
    json.dump(dataset, outfile)