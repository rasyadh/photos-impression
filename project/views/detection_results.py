from flask import (
    Blueprint,
    render_template,
    jsonify,
    session,
    redirect,
    url_for
)
from project.models.result_detection import ResultDetection
from project.models.detection import Detection

result = Blueprint('result', __name__)

@result.route('/detection_results/')
def index():
    if session.get('loggedin'):
        slides = { 1: 'acak', 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }

        try:
            results = ResultDetection.query.all()

            for r in results:
                r.category_photos = slides[r.category_photos].capitalize()

        except Exception as e:
            print('error to get detection result')
            print(e)

        return render_template('detection_results/results.html', 
            title="Hasil Percobaan", results=list(reversed(results)))
    else:
        return redirect(url_for('auth.login'))

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
