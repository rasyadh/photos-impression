import cv2
import numpy as np
from lbp import LocalBinaryPattern

face_cascade = cv2.CascadeClassifier('cascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('cascade/haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('cascade/haarcascade_mcs_mouth.xml')

data = {}
img = cv2.imread('KA.HA1.29.tiff')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.5,
    minNeighbors=5,
    minSize=(50, 50),
    flags=cv2.CASCADE_SCALE_IMAGE
)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi_gray = gray[y: y+h, x: x+w]
    roi_color = img[y: y+h, x: x+w]
    data['face'] = roi_gray

    eyes = eye_cascade.detectMultiScale(roi_gray)
    num_eye = 1
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey+ eh), (255,0,0), 2)
        if num_eye == 1:
            data['left_eye'] = roi_gray[ey: ey+eh, ex: ex+ew]
            num_eye += 1
        elif num_eye == 2:
            data['right_eye'] = roi_gray[ey: ey+eh, ex: ex+ew]
    
    mouth = mouth_cascade.detectMultiScale(roi_gray, 1.7, 11)
    for (mx, my, mw, mh) in mouth:
        my = int(my - 0.15 * mh)
        cv2.rectangle(roi_color, (mx, my), (mx + mw, my+ mh), (0,0,255), 2)
        data['mouth'] = roi_gray[my: my+mh, mx: mx+mw]

cv2.imshow('face', data['face'])
cv2.imshow('left_eye', data['left_eye'])
cv2.imshow('right_eye', data['right_eye'])
cv2.imshow('mouth', data['mouth'])
cv2.waitKey(0)
cv2.destroyAllWindows()