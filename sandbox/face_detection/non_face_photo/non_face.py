import cv2
import os

PATH = os.path.abspath(os.path.dirname(__file__)) + '\\'
face_detector = cv2.CascadeClassifier('../cascade/haarcascade_frontalface_default.xml')

for file in os.listdir():
    if file.endswith(".jpg"):
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow(file, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
