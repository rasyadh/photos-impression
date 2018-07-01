import random
import operator
import json
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify,
    request,
    session
)
from sqlalchemy import desc
from project.models import db
from project.models.result_detection import ResultDetection
from project.models.detection import Detection
from project.models.photos import Photos

detect = Blueprint('detect', __name__)

@detect.route('/expression_detection/')
def index():
    if session.get('loggedin'):    
        return render_template('main/expression_detection.html', 
            title="Deteksi Ekspresi")
    else:
        return redirect(url_for('auth.login'))

@detect.route('/expression_detection/<int:id>')
def expression_detection(id):
    picked = generate_slide(id)
    slides = { 1: 'acak', 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }

    try:
        result_detection = ResultDetection(
            category_photos=id, id_user=session['loggedin']['id_user'])
        db.session.add(result_detection)
        db.session.commit()

        result_detection = ResultDetection.query.filter_by(id_user=session['loggedin']['id_user']).order_by(desc(ResultDetection.id_result_detection)).first()
        id_result_detection = result_detection.id_result_detection

        return render_template('main/slideshow.html', 
            title="Deteksi Ekspresi", slides=picked, category=slides[id], id_res_det=id_result_detection)
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

@detect.route('/expression_detection/result/', methods=['POST'])
def result_expression_detection():
    if request.method == 'POST':
        id_result_detection = request.form['id_res_det']
        category = request.form['category']
        expression_result = request.form['data']
        photos_slide = request.form['photos']
        expression_result = json.loads(expression_result)
        photos_slide = json.loads(photos_slide)

        try:
            if expression_result:
                for expr in expression_result:
                    detection = Detection(
                        id_result_detection=id_result_detection,
                        id_photo=int(expr['id_photos']),
                        result_expression=int(expr['expression']),
                        time_detected=expr['time']
                    )

                    db.session.add(detection)
                    db.session.commit()
        except Exception as e:
            print('error to get detection result')
            print(e)

    return render_template('main/detection_result.html', 
        title="Hasil Deteksi Ekspresi", id=id_result_detection, category=category)
    
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