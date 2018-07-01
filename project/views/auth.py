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
    error = None
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
                    session['loggedin'] = {
                        'id_user': user.id_user,
                        'username': user.username
                    }

                    return redirect(url_for('main.index'))
                else:
                    error = "Username atau password salah"

                    return render_template('auth/login.html', title="Login", error=error)
            except Exception as e:
                print(e)
                error = 'Gagal Login'

                return render_template('auth/login.html', 
                    title="Login", error=error)

        return render_template('auth/login.html', 
            title="Login", error=error)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
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
                    error = 'Username sudah terpakai'
                    return render_template('auth/register.html', 
                        title="Register", error=error)
            except Exception as e:
                print(e)
                error = 'Gagal mendaftar'
                return render_template('auth/register.html', title="Register", error=error)

        return render_template('auth/register.html', title="Register", error=error)

@auth.route('/logout/')
def logout():
    session.pop('loggedin', None)

    return redirect(url_for('auth.login'))

@auth.route('/admin/', methods=['GET', 'POST'])
def login_admin():
    error = None
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
                    error = "Username atau password salah"
                    return render_template('auth/login_admin.html', 
                        title="Login Admin", error=error)
            except Exception as e:
                print(e)
                error = "Gagal Login"
                return render_template('auth/login_admin.html', 
                    title="Login Admin", error=error)

        return render_template('auth/login_admin.html', 
            title="Login Admin", error=error)

@auth.route('/admin/logout/')
def logout_admin():
    session.pop('loggedin_admin', None)

    return redirect(url_for('auth.login_admin'))