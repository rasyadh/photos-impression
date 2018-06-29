import json
from time import time
from flask import (
    Blueprint,
    Response
)
from project import app
from project import globals_var
from project.lib.eigenfaces import Eigenfaces
from project.lib.svm import SupportVectorMachine
from project.lib.face_detection import FaceDetection

stream = Blueprint('stream', __name__)

@stream.route('/feed_stream/')
def feed_stream():
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'
    FEATURE_FILE_PATH = DATASET_PATH + 'eigenfaces_jaffe_dataset.json'
    FILE_PATH = DATASET_PATH + 'feature_jaffe_dataset.json'
    globals_var.FER_DETECTED = {}

    with open(FEATURE_FILE_PATH) as data:
        data_train = json.load(data)
        data.close()

    eigenfaces = Eigenfaces(n_components=50)
    dataset = eigenfaces.prepare_data(FILE_PATH)
    pca = eigenfaces.pca_data_test(dataset)

    svm = SupportVectorMachine()
    classifier = svm.train(data_train)

    return Response(generate(FaceDetection(), pca, classifier, svm), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def generate(detect, pca, classifier, svm):
    t0 = time()

    while True: 
        feature_test = []
        face = None
        label_pred = None

        frame, face = detect.get_frame()

        if face is not None:
            face = face.flatten()
            feature_test.append(face)

            data_test = pca.transform(feature_test)
            label_pred = svm.predict(classifier, data_test)[0]

            endtime = float("{:.3f}".format(time() - t0))

            globals_var.FER_DETECTED[endtime] = label_pred
            print("{0}: {1}".format(endtime, label_pred))

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' 
            + frame + b'\r\n')