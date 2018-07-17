import cv2
import numpy as np

classifier = '../haarcascade_frontalface_default.xml'

image = cv2.imread('ha1.jpg', 0)
face_cascade = cv2.CascadeClassifier(classifier)
faces = face_cascade.detectMultiScale(
    image,
    scaleFactor=1.5,
    minNeighbors=5,
    minSize=(50, 50),
    flags=cv2.CASCADE_SCALE_IMAGE
)
for (x, y, w, h) in faces:
    print('ada')
    face = image[y : (y + h), x : (x + w)]
    face = cv2.resize(face, (120, 120))

print(face)