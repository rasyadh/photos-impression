import os
import datetime
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    session,
    request,
    jsonify
)
from werkzeug.utils import secure_filename
from project import app
from project.models import db
from project.models.photos import Photos

dashboard_photos = Blueprint('dashboard_photos', __name__)

@dashboard_photos.route('/dashboard/photos_collection/')
def index():
    if session.get('loggedin_admin'):
        try:
            photos = Photos.query.all()
            impresi = { 1: 'bahagia', 2: 'sedih', 3: 'terkejut' }
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

        return render_template('dashboard/photos_collection.html', 
            title="Koleksi Foto", photos=result)
    else:
        return redirect(url_for('auth.login_admin'))

@dashboard_photos.route('/dashboard/photos_collection/add', methods=['POST'])
def add_photo():
    result = None
    app.config['UPLOAD_FOLDER'] = app.root_path + '\static\image\photos'
    
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
        
        return redirect(url_for('dashboard_photos.index'))

    return redirect(url_for('dashboard_photos.index'))

@dashboard_photos.route('/dashboard/photos_collection/<int:id>')
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

@dashboard_photos.route('/dashboard/photos_collection/edit/<int:id>', 
    methods=['POST'])
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

        return redirect(url_for('dashboard_photos.index'))

    return redirect(url_for('dashboard_photos.index'))

@dashboard_photos.route('/dashboard/photos_collection/delete/<int:id>', 
    methods=['POST'])
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