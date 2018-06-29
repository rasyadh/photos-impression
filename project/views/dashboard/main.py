from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard/')
def index():
    if session.get('loggedin_admin'):
        return render_template('dashboard/index.html', 
            title="Dashboard Page")
    else:
        return redirect(url_for('auth.login_admin'))