import numpy as np
from numpy import linalg as LA
from numpy.linalg import eigh, solve
import cv2

#img = cv2.imread('01.pgm', 0)
img = cv2.imread('KA.HA1.29.tiff', 0)

face_cascade = cv2.CascadeClassifier('../project/cascade/haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(
    img,
    scaleFactor=1.5,
    minNeighbors=5,
    minSize=(50, 50),
    flags=cv2.CASCADE_SCALE_IMAGE
)

for (x, y, w, h) in faces:
    face = img[y: (y + h), x: (x + w)]
    face = cv2.resize(face, (20, 20))

data = face.tolist().copy()
data2 = face.tolist().copy()

# PCA cara 1
data -= np.mean(data, 0)
data /= np.std(data, 0)
C = np.cov(data)
E, V = eigh(C)
key = np.argsort(E)[::-1][:10]
E, V = E[key], V[:, key]
U = np.dot(data, V)

print('cara 1')
print(E)
print()
print(V)
print()
print(U)
print()

# PCA cara 2
data2 -= np.mean(data2, axis=0)
R = np.cov(data2, rowvar=False)
evals, evecs = eigh(R)
idx = np.argsort(evals)[::-1][:10]
print(idx)
evals, evecs = evals[idx], evecs[:, idx]

print('cara 2')
print(evals)
print()
print(evecs)
print()
print(np.dot(evecs.T, data.T).T)