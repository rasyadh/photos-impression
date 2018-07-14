from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    jsonify
)
from project.models import db
from project.models.result_detection import ResultDetection
from project.models.detection import Detection

dashboard_results = Blueprint('dashboard_results', __name__)

@dashboard_results.route('/dashboard/detection_results/')
def index():
    if session.get('loggedin_admin'):
        try:
            #results = ResultDetection.query.all()
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

        # db.session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('dashboard_results.index'))