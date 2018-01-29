import numpy as np
from numpy.linalg import eigh, solve
import cv2

class PrincipleComponentAnalysis:
    def __init__(self, classifier, num_component):
        self.classifier = classifier
        self.num_component = num_component

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
        
        return face.tolist()
    
    def mean(self, data):
        mu = data - np.mean(data, axis=0)

        return mu

    def covariance(self, mu):
        C = np.cov(mu, rowvar=False)

        return C

    def eigenfaces(self, C, mu):
        eigenvalue, eigenvector = eigh(C)
        idx = np.argsort(eigenvalue)[::-1]
        eigenvector = eigenvector[:, idx]
        eigenvalue, eigenvector = eigenvalue[idx], eigenvector[:, :self.num_component]
        U = np.dot(eigenvector.T, mu.T).T

        return U, eigenvalue, eigenvector

    def process_pca(self, data):
        w, v = LA.eig(data)
        w, v = w.real, v.real
        return w, v