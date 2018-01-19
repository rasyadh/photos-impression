import numpy as np
from numpy import linalg as LA
import cv2

img = cv2.imread('01.pgm', 0)

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

w, v = LA.eig(face)
print(w)
print(v)