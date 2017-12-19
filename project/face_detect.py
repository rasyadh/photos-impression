import cv2
import numpy as np

CASECADE_CLASSIFIER_PATH = "project/cascade/haarcascade_frontalface_default.xml"

class FaceDetect(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, frame = self.capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = cv2.CascadeClassifier(CASECADE_CLASSIFIER_PATH)

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        ) 

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()