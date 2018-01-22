import numpy as np
from numpy import linalg as LA
import cv2

class PrincipleComponentAnalysis:
    def __init__(self, classifier):
        self.classifier = classifier

    def read_images(self, path, size=None):
        face = None
        img = cv2.imread(path, 0)

        face_cascade = cv2.CascadeClassifier(self.classifier)
        faces = face_cascade.detectMultiScale(
            img,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE   
        )

        for (x, y, w, h) in faces:
            face = img[y : (y + h), x : (x + w)]
            if (size is not None):
                face = cv2.resize(face, (size, size))
        
        return face

    def process_pca(self, data):
        w, v = LA.eig(data)
        w, v = w.real, v.real
        return w, v