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
from project.globals import PHOTOS_SEQUENCE
from sqlalchemy import desc
from project.models import db
from project.models.result_detection import ResultDetection
from project.models.detection import Detection
from project.models.detection_photo import DetectionPhoto
from project.models.photos import Photos

detect = Blueprint('detect', __name__)

@detect.route('/expression_detection/')
def index():
    if session.get('loggedin'):
        slides = generate_slide()

        try:
            result_detection = ResultDetection(id_user=session['loggedin']['id_user'])
            db.session.add(result_detection)
            db.session.commit()

            result_detection = ResultDetection.query.filter_by(
                id_user=session['loggedin']['id_user']).order_by(
                    desc(ResultDetection.id_result_detection)).first()
            id_result_detection = result_detection.id_result_detection

            return render_template('main/slideshow.html', 
                title="Deteksi Ekspresi", slides=slides, id_res_det=id_result_detection)
        except Exception as e:
            print('error to add result detection')
            print(e)

        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('auth.login'))

def generate_slide():
    photo_slides, sequence_1, sequence_2 = [], [], []
    count, max, threshold = 0, 5, 10

    try:
        photos = Photos.query.all()

        for photo in photos:    
            temp = {
                'id': photo.id_photo,
                'photo_name': photo.photo_name,
                'photo_url': photo.photo_url,
                'impression': photo.comment_impression
            }
            
            if count == threshold:
                count = 0

            if count < max:
                sequence_1.append(temp)
                count += 1
            elif count >= max and count < threshold:
                sequence_2.append(temp)
                count += 1

        photo_slides = sequence_1 + sequence_2
    except Exception as e:
        print(e)
    
    return photo_slides

@detect.route('/expression_detection/result/', methods=['POST'])
def result_expression_detection():
    time_dict = {}
    per_photo_time = []
    photos_dict = PHOTOS_SEQUENCE.copy()

    if request.method == 'POST':
        id_result_detection = request.form['id_res_det']
        expression_result = request.form['data']
        photos_slide = request.form['photos']
        expression_result = json.loads(expression_result)
        photos_slide = json.loads(photos_slide)

        for i in range(len(expression_result)):
            key = expression_result[i]['time'].split(".")
            sec = int(key[0]) + 1

            if sec not in time_dict:
                time_dict[sec] = [expression_result[i]['expression']]
            else:
                time_dict[sec].append(expression_result[i]['expression'])

        for sec in range(1, 61):
                if sec not in time_dict.keys():
                    time_dict[sec] = [0]

        for i in range(1, 61, 2):
            per_photo_time.append(time_dict[i] + time_dict[i+1])

        for i in range(len(photos_dict)):
            if len(per_photo_time[i]) > 1:
                temp = {}
                unique = list(set(per_photo_time[i]))

                for j in unique:
                    temp[j] = per_photo_time[i].count(j)
                photos_dict[i]['expression'] = max(temp.items(), key=operator.itemgetter(1))[0]
            else:
                photos_dict[i]['expression'] = per_photo_time[i][0]

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
            
            if photos_dict:
                for photo in photos_dict:
                    detection_photo = DetectionPhoto(
                        id_result_detection=id_result_detection,
                        id_photo=photo['id_photo'],
                        result_expression=photo['expression']
                    )

                    db.session.add(detection_photo)
                db.session.commit()
        except Exception as e:
            print(e)

    return render_template('main/detection_result.html', 
        title="Hasil Deteksi Ekspresi", id=id_result_detection)
    
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