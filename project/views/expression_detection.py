import random
import operator
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify
)
from project import globals_var
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
    print(globals_var.FER_DETECTED)
    result = {}

    for key, value in globals_var.FER_DETECTED.items():
        sec = int(str(key).split('.')[0]) + 1

        if sec not in result.keys():
            result[sec] = []

        if sec in result.keys():
            result.get(sec).append(value)

    for key, value in result.items():
        if len(value) > 1:
            temp = {}
            unique = list(set(value))

            for i in unique:
                temp[i] = value.count(i)
            
            result[key] = max(temp.items(), key=operator.itemgetter(1))[0]
        else:
            result[key] = value[0]
        
    print(result)

    try:
        result_detection = ResultDetection.query.order_by(
            desc(ResultDetection.id_result_detection)).first()
        id = result_detection.id_result_detection

        if result:
            for key, value in result.items():
                detection = Detection(
                    id_result_detection=id,
                    result_expression=int(value),
                    time_detected=key
                )
                db.session.add(detection)
                db.session.commit()
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