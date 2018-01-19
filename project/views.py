import os, datetime

from flask import Flask, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import make_response, abort, session

from project import app
from project.core import db
from project.models import *

from project.face_detect import FaceDetect

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/detect_expression')
def main():
    return render_template('main.html', title="Deteksi Ekspresi")

@app.route('/main_detect/<int:id>')
def detect(id):
    return render_template('slideshow.html', title="Deteksi Ekspresi")

@app.route('/detect_result/')
def detect_result():
    return render_template('detect_result.html', title="Hasil Deteksi Ekspresi")

def generate(detect):
    while True:
        frame = detect.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed_stream/')
def feed_stream():
    return Response(generate(FaceDetect()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/photos/')
def photos():
    try:
        photos = Photos.query.all()
        impresi = { 2: 'happy', 3: 'sad', 4: 'surprise' }
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
    results = None
    return render_template('results.html', title="Hasil Percobaan", results=results)

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

@app.route('/admin/feature')
def extraction_feature():
    if session.get('loggedin'):
        return render_template('admin/feature_extraction.html', title="Ekstraksi Fitur")
    return redirect(url_for('login'))

@app.route('/feature')
def feature():
    data = None
    with open('tes_pca/feature.json') as f:
        data = json.load(f)
        f.close()
    return jsonify(data)

@app.route('/admin/photos/')
def photos_collection():
    if session.get('loggedin'):
        try:
            photos = Photos.query.all()
            impresi = { 2: 'happy', 3: 'sad', 4: 'surprise' }
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