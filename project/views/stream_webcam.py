import json
import requests
from flask import (
    Blueprint,
    Response
)
from project import app
from project.lib.eigenfaces import Eigenfaces
from project.lib.svm import SupportVectorMachine
from project.lib.face_detection import FaceDetection

stream = Blueprint('stream', __name__)

@stream.route('/feed_stream/')
def feed_stream():
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'
    FILE_PATH = DATASET_PATH + 'feature_jaffe_dataset.json'
    # DATASET_PATH = app.root_path + '\\static\image\dataset\indonesia\\'
    # FILE_PATH = DATASET_PATH + 'feature_indonesia_dataset.json'

    eigenfaces = Eigenfaces(n_components=50)
    # eigenfaces = Eigenfaces(n_components=30)
    dataset = eigenfaces.prepare_data(FILE_PATH)
    pca, train = eigenfaces.pca_data_test(dataset)
    
    datas = {
        'eigenvectors': train.tolist(),
        'label': dataset['label']
    }

    with open(DATASET_PATH + 'eigenfaces_jaffe_dataset.json', 'w') as outfile:
        json.dump(datas, outfile)
        outfile.close()

    svm = SupportVectorMachine()
    classifier = svm.train(train, dataset['label'])

    return Response(generate(FaceDetection(), pca, classifier, svm),    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate(detect, pca, classifier, svm):
    while True:     
        feature_test = []
        result_expression = []
        face = None
        label_pred = None

        frame, face = detect.get_frame()

        if face is not None:
            face = face.flatten()
            feature_test.append(face)

            data_test = pca.transform(feature_test)
            label_pred = svm.predict(classifier, data_test)[0]

            print("expression : {0}".format(label_pred))

            result_expression.append(label_pred)

            requests.get("http://localhost:3000/kirimData?data="+json.dumps(result_expression, indent=4, default=str)).json()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' 
            + frame + b'\r\n')