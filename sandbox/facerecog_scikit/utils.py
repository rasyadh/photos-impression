import cv2
import numpy as np

class Utils:
    def __init__(self, classifier):
        self.classifier = classifier

    def read_images(self, path, size=None):
        face = None

        image = cv2.imread(path, 0)
        face_cascade = cv2.CascadeClassifier(self.classifier)
        faces = face_cascade.detectMultiScale(
            image,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            face = image[y : (y + h), x : (x + w)]
            if (size is not None):
                face = cv2.resize(face, (size, size))

        return face