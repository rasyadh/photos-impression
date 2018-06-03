import random
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify
)
from sqlalchemy import desc
from project.models import db
from project.models.result_detection import ResultDetection
from project.models.detection import Detection
from project.models.photos import Photos

detect = Blueprint('detect', __name__)

@detect.route('/expression_detection/')
def index():
    return render_template('main/expression_detection.html', 
        title="Deteksi Ekspresi")

@detect.route('/expression_detection/<int:id>')
def expression_detection(id):
    picked = generate_slide(id)
    slides = { 1: 'acak', 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }

    try:
        result_detection = ResultDetection(category_photos=id)
        db.session.add(result_detection)
        db.session.commit()

        return render_template('main/slideshow.html', 
            title="Deteksi Ekspresi", slides=picked, category=slides[id])
    except Exception as e:
        print('error to add result detection')
        print(e)

    redirect(url_for('detect.index'))

def generate_slide(id):
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

@detect.route('/expression_detection/result/')
def result_expression_detection():
    try:
        result_detection = ResultDetection.query.order_by(
            desc(ResultDetection.id_result_detection)).first()
        id = result_detection.id_result_detection

    except Exception as e:
        print('error to get detection result')
        print(e)

    return render_template('main/detection_result.html', 
        title="Hasil Deteksi Ekspresi", id=id)
    
@detect.route('/expression_detection/result_detection/<string:id>')
def get_result_expression_detection(id):
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
        print(e)
    
    return jsonify(result)