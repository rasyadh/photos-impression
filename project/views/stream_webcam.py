import json
from time import time
from flask import (
    Blueprint,
    Response
)
from project import app
from project.lib.eigenfaces import Eigenfaces
from project.lib.svm import SupportVectorMachine
from project.lib.face_detection import FaceDetection
from project.models import db
from sqlalchemy import desc
from project.models.result_detection import ResultDetection
from project.models.detection import Detection

stream = Blueprint('stream', __name__)

@stream.route('/feed_stream/')
def feed_stream():
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'
    FEATURE_FILE_PATH = DATASET_PATH + 'eigenfaces_jaffe_dataset.json'
    FILE_PATH = DATASET_PATH + 'feature_jaffe_dataset.json'

    with open(FEATURE_FILE_PATH) as data:
        data_train = json.load(data)
        data.close()

    eigenfaces = Eigenfaces(n_components=50)
    dataset = eigenfaces.prepare_data(FILE_PATH)
    pca = eigenfaces.pca_data_test(dataset)

    svm = SupportVectorMachine()
    classifier = svm.train(data_train)

    result_detection = ResultDetection.query.order_by(
        desc(ResultDetection.id_result_detection)).first()
    id_rd = result_detection.id_result_detection

    return Response(generate(FaceDetection(), pca, classifier, svm, id_rd), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def generate(detect, pca, classifier, svm, id_rd):
    t0 = time()
    FerDetected = dict()

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

            FerDetected = {
                endtime: label_pred
            }
            print(FerDetected)

            try:
                detection = Detection(
                    id_result_detection=id_rd, 
                    result_expression=int(label_pred), 
                    time_detected=endtime
                )
                db.session.add(detection)
                db.session.commit()
            except Exception as e:
                print('error to add detection')
                print(e)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' 
            + frame + b'\r\n')