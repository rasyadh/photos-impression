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
    slides = { 1: 'acak', 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }

    if session.get('loggedin_admin'):
        try:
            results = ResultDetection.query.all()

            for r in results:
                r.category_photos = slides[r.category_photos].capitalize()

            by_category = { 'Acak': 0, 'Bahagia': 0, 'Sedih': 0, 'Terkejut': 0 }
            for res in results:
                if res.category_photos == 'Acak':
                    by_category['Acak'] += 1
                elif res.category_photos == 'Bahagia':
                    by_category['Bahagia'] += 1
                elif res.category_photos == 'Sedih':
                    by_category['Sedih'] += 1
                elif res.category_photos == 'Terkejut':
                    by_category['Terkejut'] += 1

            return render_template('dashboard/detection_results.html', 
                title='Hasil Percobaan', results=list(reversed(results)), by_category=by_category)
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