from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('loggedin'):
        return render_template('main/index.html', title="Home")
    else:
        return redirect(url_for('auth.login'))