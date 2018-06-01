from flask import (
    Blueprint,
    render_template,
    jsonify
)
from project.models.result_detection import ResultDetection
from project.models.detection import Detection

result = Blueprint('result', __name__)

@result.route('/detection_results/')
def index():
    try:
        results = ResultDetection.query.all()
    except Exception as e:
        print('error to get detection result')
        print(e)

    return render_template('detection_results/results.html', 
        title="Hasil Percobaan", results=results)

@result.route('/detection_results/<string:id>')
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