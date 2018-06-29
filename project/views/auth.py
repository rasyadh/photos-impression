from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    session
)
from project.models import db
from project.models.admin import Admin
from project.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if session.get('loggedin'):
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            try:
                user = User.query.filter_by(
                    username=username, password=password).first()

                if user is not None:
                    session['loggedin'] = username

                    return redirect(url_for('main.index'))
                else:
                    return render_template('auth/login.html', title="Login")
            except Exception as e:
                print(e)
                return render_template('auth/login.html', 
                    title="Login")

        return render_template('auth/login.html', 
            title="Login")

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if session.get('loggedin'):
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            try:
                if not User.query.filter_by(username=username).first():
                    user = User(username=username, password=password)
                    db.session.add(user)
                    db.session.commit()

                    return redirect(url_for('auth.login'))
                else:
                    return render_template('auth/register.html', 
                        title="Register")
            except Exception as e:
                print(e)
                return render_template('auth/register.html', title="Register")

        return render_template('auth/register.html', title="Register")

@auth.route('/logout/')
def logout():
    session.pop('loggedin', None)

    return redirect(url_for('auth.login'))

@auth.route('/admin/', methods=['GET', 'POST'])
def login_admin():
    if session.get('loggedin_admin'):
        return redirect(url_for('dashboard.index'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            try:
                user = Admin.query.filter_by(
                    username=username, password=password).first()

                if user is not None:
                    session['loggedin_admin'] = username

                    return redirect(url_for('dashboard.index'))
                else:
                    return render_template('auth/login_admin.html', 
                        title="Login Admin")
            except Exception as e:
                print(e)
                return render_template('auth/login_admin.html', 
                    title="Login Admin")

        return render_template('auth/login_admin.html', 
            title="Login Admin")

@auth.route('/admin/logout/')
def logout_admin():
    session.pop('loggedin_admin', None)

    return redirect(url_for('auth.login_admin'))