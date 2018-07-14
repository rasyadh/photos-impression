from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    jsonify
)
from project.models.user import User
from project.models.result_detection import ResultDetection
from project.models.detection_photo import DetectionPhoto

user = Blueprint('user', __name__)

@user.route('/dashboard/user/')
def index():
    if session.get('loggedin_admin'):
        try:
            users = User.query.all()

            return render_template('dashboard/user.html', 
                title='Pengguna', users=users)
        except Exception as e:
            print('error to get detection result')
            print(e)

    return redirect(url_for('auth.login_admin'))

@user.route('/dashboard/user/expression/<int:id>')
def get_expression(id):
    try:
        res_det = ResultDetection.query.filter_by(id_user=id).first()
        det_photo = DetectionPhoto.query.filter_by(id_result_detection=res_det.id_result_detection).all()

        data = []
        for d in det_photo:
            temp = {
                'result_expression': d.result_expression,
                'id_photo': d.id_photo
            }
            data.append(temp)

        result = {
            'data': data,
            'date': res_det.created_at
        }

    except Exception as e:
        print(e)

    return jsonify(result)