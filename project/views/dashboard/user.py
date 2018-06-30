from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for
)
from project.models.user import User

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