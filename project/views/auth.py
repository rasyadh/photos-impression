from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    session
)
from project.models.admin import Admin

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if session.get('loggedin'):
        return redirect(url_for('dashboard.index'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            try:
                user = Admin.query.filter_by(
                    username=username, password=password).first()

                if user is not None:
                    session['loggedin'] = username

                    return redirect(url_for('dashboard.index'))
                else:
                    return render_template('auth/login.html', 
                        title="Login Admin")
            except Exception as e:
                print(e)
                return render_template('auth/login.html', 
                    title="Login Admin")

        return render_template('auth/login.html', 
            title="Login Admin")

@auth.route('/logout/')
def logout():
    session.pop('loggedin', None)

    return redirect(url_for('main.index'))