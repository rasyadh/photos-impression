from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    jsonify
)
from project.models.result_detection import ResultDetection
from project.models.detection import Detection

dashboard_results = Blueprint('dashboard_results', __name__)

@dashboard_results.route('/dashboard/detection_results/')
def index():
    if session.get('loggedin'):
        try:
            results = ResultDetection.query.all()

            return render_template('dashboard/detection_results.html', 
                title='Hasil Percobaan', results=results)
        except Exception as e:
            print('error to get detection result')
            print(e)

    # return redirect(url_for('auth.login'))
    print('sefs')

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