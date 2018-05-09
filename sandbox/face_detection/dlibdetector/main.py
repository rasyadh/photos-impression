import cv2
import dlib
import numpy as np

capture = cv2.VideoCapture(0)

size = 50
def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    return (x, y, w, h)

detector = dlib.get_frontal_face_detector()

# image = cv2.imread('02.jpg', 0)
while True:
    succes, frame = capture.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(image, 0)

    for i, rect in enumerate(rects):
        (x, y, w, h) = rect_to_bb(rect)
        face = image[y : (y + h), x : (x + w)]
        face = cv2.resize(face, (size, size))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('face', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cv2.imshow('face', face)
# cv2.waitKey(0)
capture.release()
cv2.destroyAllWindows()