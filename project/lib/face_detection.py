from imutils import (
    face_utils,
    resize
)
import cv2
import numpy as np
import dlib

class FaceDetection(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('project/face_landmark/shape_predictor_68_face_landmarks.dat')

    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def rect_to_bb(self, rect):
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        return (x, y, w, h)

    def get_landmark(self):
        feature, size = [], 120
        success, frame = self.capture.read()

        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale image
            rects = self.detector(gray, 1)

            # loop over the face detections
            for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the landmark (x, y)-coordinates to a NumPy array
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # loop over the face parts individually
                for (name, (i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                    for (x,y) in shape[i:j]:
                        if name == "mouth":
                            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
                            feature.append(x)
                            feature.append(y)
                        elif name == "left_eyebrow":
                            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
                            feature.append(x)
                            feature.append(y)
                        elif name == "right_eyebrow":
                            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
                            feature.append(x)
                            feature.append(y)
                        elif name == "left_eye":
                            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
                            feature.append(x)
                            feature.append(y)
                        elif name == "right_eye":
                            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
                            feature.append(x)
                            feature.append(y)

            ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes(), feature

    def get_frame(self):
        face, size = None, 120
        success, frame = self.capture.read()

        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)

            for i, rect in enumerate(rects):
                (x, y, w, h) = self.rect_to_bb(rect)
                face = gray[y : (y + h), x : (x + w)]

                if size is not None:
                    face = cv2.resize(face, (size, size))

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, jpeg = cv2.imencode('.jpg', frame)
            
        return jpeg.tobytes(), face