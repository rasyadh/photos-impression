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
from project.lib.feature_landmark import FeatureLandmark
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

@extraction.route('/dashboard/feature_extraction/read_dataset/<string:data>', methods=['GET'])
def read_dataset(data):
    print('read ' + data + ' dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\\' + data + '\\'

    utils = FeatureDataset()
    utils.read_dataset(DATASET_PATH, data)

    print("done in %0.5fs" % (time() - t0))
    print("file dataset and feature created")

    return redirect(url_for('extraction.index'))

@extraction.route('/dashboard/feature_extraction/process/<string:idata>', methods=['GET'])
def process_feature(idata):
    print('process eigenfaces of ' + idata + ' dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\\' + idata + '\\'
    # DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'
    if idata == 'jaffe':
        FILE_PATH = DATASET_PATH + 'feature_jaffe_dataset.json'
        eigenfaces = Eigenfaces(n_components=50)
    else:
        FILE_PATH = DATASET_PATH + 'feature_indonesia_dataset.json'
        eigenfaces = Eigenfaces(n_components=30)

    data = eigenfaces.prepare_data(FILE_PATH)
    eigenvectors = eigenfaces.principle_component_analysis(data)

    datas = {
        'eigenvectors': eigenvectors.tolist(),
        'label': data['label']
    }

    with open(DATASET_PATH + 'eigenfaces_' + idata + '_dataset.json', 'w') as outfile:
        json.dump(datas, outfile)
        outfile.close()

    print("done in %0.5fs" % (time() - t0))

    return redirect(url_for('extraction.index'))

@extraction.route('/dashboard/feature_extraction/features/<string:data>')
def show_feature(data):
    datas = None
    if data == 'jaffe':
        DATASET_FILE_PATH = 'project/static/image/dataset/jaffe/eigenfaces_jaffe_dataset.json'
    else:
        DATASET_FILE_PATH = 'project/static/image/dataset/indonesia/eigenfaces_indonesia_dataset.json'
    
    with open(DATASET_FILE_PATH) as f:
        datas = json.load(f)
        f.close()

    return jsonify(datas)

@extraction.route('/dashboard/feature_extraction/landmark/<string:dataset>')
def extract_landmark(dataset):
    print('read ' + dataset + ' dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\\' + dataset + '\\'

    utils = FeatureLandmark()
    utils.read_dataset(DATASET_PATH, dataset)

    print("done in %0.5fs" % (time() - t0))
    print("file dataset and feature created")

    return redirect(url_for('extraction.index'))

@extraction.route('/dashboard/feature_extraction/features_landmark/<string:dataset>')
def show_feature_landmark(dataset):
    datas = None
    if dataset == 'jaffe':
        DATASET_FILE_PATH = 'project/static/image/dataset/jaffe/feature_landmark_jaffe_dataset.json'
    else:
        DATASET_FILE_PATH = 'project/static/image/dataset/indonesia/feature_landmark_indonesia_dataset.json'
    
    with open(DATASET_FILE_PATH) as f:
        datas = json.load(f)
        f.close()

    return jsonify(datas)