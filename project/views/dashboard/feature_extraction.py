from time import time
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    session,
    json,
    jsonify
)
from project import app
from project.lib.feature_dataset import FeatureDataset
from project.lib.eigenfaces import Eigenfaces

extraction = Blueprint('extraction', __name__)

@extraction.route('/dashboard/feature_extraction/')
def index():
    if session.get('loggedin_admin'):
        data = None
        DATASET_FILE_PATH = app.root_path + '\\static\image\dataset\jaffe-jpg\dataset_jaffe.json'

        try:
            with open(DATASET_FILE_PATH) as f:
                data = json.load(f)
                f.close()
        except Exception as e:
            print('error to read json')
            print(e)

        return render_template('dashboard/feature_extraction.html', 
            title="Ekstraksi Fitur", datasets=data)

    return redirect(url_for('auth.login_admin'))

@extraction.route('/dashboard/feature_extraction/read_dataset', methods=['GET'])
def read_dataset():
    print('read jaffe dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'

    utils = FeatureDataset()
    utils.read_jaffe_dataset(DATASET_PATH)

    print("done in %0.5fs" % (time() - t0))
    print("file dataset jafee and feature jaffe created")

    return redirect(url_for('extraction.index'))

@extraction.route('/dashboard/feature_extraction/process', methods=['GET'])
def process_feature():
    print('process eigenfaces of jaffe dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'
    FILE_PATH = DATASET_PATH + 'feature_jaffe_dataset.json'

    eigenfaces = Eigenfaces(n_components=50)
    data = eigenfaces.prepare_data(FILE_PATH)
    eigenvectors = eigenfaces.principle_component_analysis(data)

    datas = {
        'eigenvectors': eigenvectors.tolist(),
        'label': data['label']
    }

    with open(DATASET_PATH + 'eigenfaces_jaffe_dataset.json', 'w') as outfile:
        json.dump(datas, outfile)
        outfile.close()

    print("done in %0.5fs" % (time() - t0))

    return redirect(url_for('extraction.index'))

@extraction.route('/dashboard/feature_extraction/features/')
def show_feature():
    data = None
    DATASET_FILE_PATH = 'project/static/image/dataset/jaffe/eigenfaces_jaffe_dataset.json'
    
    with open(DATASET_FILE_PATH) as f:
        data = json.load(f)
        f.close()

    return jsonify(data)