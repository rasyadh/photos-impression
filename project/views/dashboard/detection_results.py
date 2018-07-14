import operator
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    jsonify
)
from project.globals import PHOTOS_SEQUENCE
from project.models import db
from project.models.result_detection import ResultDetection
from project.models.detection import Detection
from project.models.detection_photo import DetectionPhoto

dashboard_results = Blueprint('dashboard_results', __name__)

@dashboard_results.route('/dashboard/detection_results/')
def index():
    if session.get('loggedin_admin'):
        try:
            result = db.engine.execute("SELECT rd.id_result_detection, rd.id_user, u.username, rd.created_at FROM result_detection rd, user u WHERE u.id_user = rd.id_user")

            results = []
            for res in result:
                temp = {
                    'id_result_detection': res[0],
                    'id_user': res[1],
                    'username': res[2],
                    'created_at': res[3]
                }
                results.append(temp)

            return render_template('dashboard/detection_results.html', 
                title='Hasil Percobaan', results=list(reversed(results)))
        except Exception as e:
            print('error to get detection result')
            print(e)

    return redirect(url_for('auth.login_admin'))

@dashboard_results.route('/dashboard/detection_results/<string:id>')
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

@dashboard_results.route('/dashboard/detection_results/delete/<int:id>')
def delete_result(id):    
    try:
        result_detection = ResultDetection.query.filter_by(id_result_detection=id).first()
        db.session.delete(result_detection)

        detection = Detection.query.filter_by(id_result_detection=id).all()
        for det in detection:
            db.session.delete(det)

        db.session.commit()
    except Exception as e:
        print(e)
    
    return redirect(url_for('dashboard_results.index'))

@dashboard_results.route('/dashboard/detection_results/tes')
def tes():
    try:
        result_detection = ResultDetection.query.all()
        print(result_detection)

        for res in result_detection:
            detection = Detection.query.filter_by(id_result_detection=res.id_result_detection).all()

            expression_result = []
            for det in detection:
                temp = {
                    'time': str(det.time_detected),
                    'expression': det.result_expression
                }
                expression_result.append(temp)

            photos_dict = PHOTOS_SEQUENCE.copy()
            time_dict = {}
            per_photo_time = []

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

            for photo in photos_dict:
                det_photo = DetectionPhoto(
                    id_result_detection=res.id_result_detection,
                    id_photo=photo['id_photo'],
                    result_expression=photo['expression']
                )
                db.session.add(det_photo)

            db.session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('dashboard_results.index'))