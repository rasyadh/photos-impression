from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for
)

statistic = Blueprint('statistic', __name__)

@statistic.route('/dashboard/statistic/')
def index():
    if session.get('loggedin_admin'):
        return render_template('dashboard/statistic.html', 
            title='Statistik')

    return redirect(url_for('auth.login_admin'))