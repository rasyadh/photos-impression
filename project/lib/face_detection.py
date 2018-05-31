import cv2
import numpy as np
import dlib

detector = dlib.get_frontal_face_detector()

class FaceDetection(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def rect_to_bb(self, rect):
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        return (x, y, w, h)

    def get_frame(self):
        face, size = None, 50
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