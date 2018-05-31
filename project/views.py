import os, datetime
import random
from time import time

import numpy as np

from flask import Flask, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import make_response, abort, session
from werkzeug.utils import secure_filename
from sqlalchemy import desc

from project import app
from project.core import db
from project.models import *

from project.face_detection import FaceDetection
from project.utils import Utils
from project.eigenfaces import Eigenfaces
from project.pca import PrincipleComponentAnalysis
from project.svm import SupportVectorMachine

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/detect_expression')
def main():
    return render_template('main.html', title="Deteksi Ekspresi")

@app.route('/main_detect/<int:id>')
def detect(id):
    picked = random_slide(id)
    slides = { 1: 'acak', 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }

    try:
        result_detection = ResultDetection(category_photos=id)
        db.session.add(result_detection)
        db.session.commit()

        return render_template('slideshow.html', title="Deteksi Ekspresi", slides=picked, category=slides[id])
    except Exception as e:
        print('error to add result detection')
        print(e)

    redirect(url_for('main'))

def random_slide(id):
    counter, max = 0, 6
    slideshow, temp, choiche = {}, [], []
    try:
        if id == 1:
            photos = Photos.query.all()
        else:
            photos = Photos.query.filter_by(comment_impression=id).all()
    except Exception as e:
        print('error to query photo')
        print(e)

    for i in range(0, len(photos)):
        temp.append(i)
    while counter < max:
        rdm = random.choice(temp)
        temp.remove(rdm)
        slideshow = {
            'id': photos[rdm].id_photo,
            'photo_name': photos[rdm].photo_name,
            'photo_url': photos[rdm].photo_url,
            'impression': photos[rdm].comment_impression
        }
        choiche.append(slideshow)
        counter += 1

    return choiche

@app.route('/detect_result/')
def detect_result():
    try:
        result_detection = ResultDetection.query.order_by(desc(ResultDetection.id_result_detection)).first()
        id = result_detection.id_result_detection

        detection = Detection.query.filter_by(id_result_detection=id).all()
    except Exception as e:
        print('error to get detection result')
        print(e)

    return render_template('detect_result.html', title="Hasil Deteksi Ekspresi", result=detection)

def generate(detect, pca, classifier, svm, id_rd):
    t0 = time()
    FerDetected = dict()
    while True: 
        feature_test = []
        face = None
        label_pred = None

        # frame, face = detect.get_frame()
        frame, face = detect.get_frame_dlib()

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
                detection = Detection(id_result_detection=id_rd, result_expression=int(label_pred), time_detected=endtime)
                db.session.add(detection)
                db.session.commit()
            except Exception as e:
                print('error to add detection')
                print(e)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed_stream/')
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

    result_detection = ResultDetection.query.order_by(desc(ResultDetection.id_result_detection)).first()
    id_rd = result_detection.id_result_detection

    return Response(generate(FaceDetection(), pca, classifier, svm, id_rd), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/photos/')
def photos():
    try:
        photos = Photos.query.all()
        impresi = { 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }
        result, data = [], {}
        for p in photos:
            if p.comment_impression in impresi:
                p.comment_impression = impresi[p.comment_impression]
            data = {
                'id_photo': p.id_photo,
                'photo_name': p.photo_name,
                'photo_url': p.photo_url,
                'source_url': p.source_url,
                'comment_impression': p.comment_impression
            }
            result.append(data)
            data = {}
    except Exception as e:
        print('error query photos')
        print(e)
    return render_template('photos.html', title="Foto Percobaan", photos=result)

@app.route('/results/')
def result():
    try:
        results = ResultDetection.query.all()
    except Exception as e:
        print('error to get result detection')
        print(e)

    return render_template('results.html', title="Hasil Percobaan", results=results)

@app.route('/results/<string:id>')
def result_detail(id):
    try:
        detection = Detection.query.filter_by(id_result_detection=int(id)).all()
        result, data = [], {}
        for d in detection:
            data = {
                'result_expression': d.result_expression,
                'time_detected': d.time_detected
            }
            result.append(data)
            data = {}
    except Exception as e:
        print('error to qurey expression')
        print(e)
    return jsonify(result)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if session.get('loggedin'):
        return redirect(url_for('admin'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            try:
                user = Admin.query.filter_by(username=username, password=password).first()
                if user is not None:
                    session['loggedin'] = username
                    return redirect(url_for('admin'))
                else:
                    return render_template('login.html', title="Login Admin")
            except:
                return 'error query'
        return render_template('login.html', title="Login Admin")

@app.route('/logout/')
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('index'))

# Admin
@app.route('/admin/')
def admin():
    if session.get('loggedin'):
        return render_template('admin/admin.html', title="Admin Page")
    else:
        return redirect(url_for('login'))

@app.route('/admin/expression')
def expression():
    if session.get('loggedin'):
        try:
            expression = Expression.query.all()
        except Exception as e:
            print('error to query expression')
            print(e)
        return render_template('admin/expression.html', title="Data Ekspresi", expression=expression)
    return redirect(url_for('login'))

@app.route('/admin/expression/<string:id>', methods=['GET'])
def get_expression(id):
    try:
        expression = Expression.query.filter_by(id_expression=int(id)).first()
        data = {}
        data = {
            'id_expression': expression.id_expression,
            'expression_name': expression.expression_name
        }
    except Exception as e:
        print('error to qurey expression')
        print(e)
    return jsonify(data)

@app.route('/admin/expression/edit/<int:id>', methods=['POST'])
def edit_expression(id):
    if request.method == 'POST':
        try:
            expression = Expression.query.filter_by(id_expression=id).first()
            expression.expression_name = request.form.get('name')
            expression.updated_at = datetime.datetime.now()
            db.session.commit()
        except Exception as e:
            print('error to update expression')
            print(e)
        return redirect(url_for('expression'))
    return redirect(url_for('expression'))

@app.route('/admin/expression/add', methods=['POST'])
def add_expression():
    if request.method == 'POST':
        try:
            expression = Expression(expression_name=request.form.get('name'))
            db.session.add(expression)
            db.session.commit()
        except Exception as e:
            print('error to add expression')
            print(e)
        return redirect(url_for('expression'))    
    return redirect(url_for('expression'))

@app.route('/admin/feature/')
def extraction_feature():
    if session.get('loggedin'):
        data = None
        DATASET_FILE_PATH = app.root_path + '\\static\image\dataset\jaffe-jpg\dataset_jaffe.json'
        try:
            with open(DATASET_FILE_PATH) as f:
                data = json.load(f)
                f.close()
        except Exception as e:
            print('error to read json')
            print(e)
        return render_template('admin/feature_extraction.html', title="Ekstraksi Fitur", datasets=data)
    return redirect(url_for('login'))

@app.route('/admin/feature/read_dataset', methods=['GET'])
def read_dataset():
    print('read jaffe dataset...')

    t0 = time()
    DATASET_PATH = app.root_path + '\\static\image\dataset\jaffe\\'

    utils = Utils()
    utils.read_jaffe_dataset(DATASET_PATH)

    print("done in %0.5fs" % (time() - t0))
    print("file dataset jafee and feature jaffe created")

    return redirect(url_for('extraction_feature'))

@app.route('/admin/feature/process', methods=['GET'])
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

    return redirect(url_for('extraction_feature'))

@app.route('/admin/feature/expression/')
def feature():
    data = None
    DATASET_FILE_PATH = 'project/static/image/dataset/jaffe/eigenfaces_jaffe_dataset.json'
    with open(DATASET_FILE_PATH) as f:
        data = json.load(f)
        f.close()
    return jsonify(data)

@app.route('/admin/photos/')
def photos_collection():
    if session.get('loggedin'):
        try:
            photos = Photos.query.all()
            impresi = { 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }
            result, data = [], {}
            for p in photos:
                if p.comment_impression in impresi:
                    p.comment_impression = impresi[p.comment_impression]
                data = {
                    'id_photo': p.id_photo,
                    'photo_name': p.photo_name,
                    'photo_url': p.photo_url,
                    'source_url': p.source_url,
                    'comment_impression': p.comment_impression
                }
                result.append(data)
                data = {}
        except Exception as e:
            print('error query photos')
            print(e)
        return render_template('admin/photos_collection.html', title="Koleksi Foto", photos=result)
    else:
        return redirect(url_for('login'))

@app.route('/admin/photos/add', methods=['POST'])
def add_photo():
    result = None
    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + '\static\image\photos'
    if request.method == 'POST':
        file = request.files['photo']
        name = 'photo-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        savedir = os.path.join(app.config['UPLOAD_FOLDER'], name)
        file.save(savedir)

        try:
            photo = Photos(
                photo_name=name, 
                photo_url='/static/image/photos/' + name, 
                source_url=request.form.get('source'), 
                comment_impression=request.form.get('impression')
            )
            db.session.add(photo)
            db.session.commit()
        except Exception as e:
            print('error to add photo')
            print(e)
        
        return redirect(url_for('photos_collection'))
    return redirect(url_for('photos_collection'))

@app.route('/admin/photos/<int:id>', methods=['GET'])
def get_photo(id):
    try:
        photo = Photos.query.filter_by(id_photo=id).first()
        data = {}
        data = {
            'id_photo': photo.id_photo,
            'photo_url': photo.photo_url,
            'source_url': photo.source_url,
            'comment_impression': photo.comment_impression
        }
    except Exception as e:
        print('error to qurey photo')
        print(e)
    return jsonify(data)

@app.route('/admin/photos/edit/<int:id>', methods=['POST'])
def edit_photo(id):
    if request.method == 'POST':
        try:
            photo = Photos.query.filter_by(id_photo=id).first()
            photo.source_url = request.form.get('source')
            photo.comment_impression = request.form.get('impression')
            db.session.commit()
        except Exception as e:
            print('error to update photo')
            print(e)
        return redirect(url_for('photos_collection'))
    return redirect(url_for('photos_collection'))

@app.route('/admin/photos/delete/<int:id>', methods=['POST'])
def delete_photo(id):
    result = False
    try:
        photo = Photos.query.filter_by(id_photo=id).first()
        db.session.delete(photo)
        db.session.commit()
        result = True
    except Exception as e:
        print('error to delete photo')
        print(e)
    return jsonify({'status': result})

@app.route('/admin/result')
def result_detection():
    if session.get('loggedin'):
        results = None
        return render_template('admin/result_detection.html', title='Hasil Percobaan')
    return redirect(url_for('login'))