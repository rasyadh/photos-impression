import datetime
from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
    jsonify,
    request,
    session
)
from project.models import db
from project.models.expression import Expression

expression = Blueprint('expression', __name__)

@expression.route('/dashboard/expression/')
def index():
    if session.get('loggedin_admin'):
        try:
            expression = Expression.query.all()
        except Exception as e:
            print('error to query expression')
            print(e)

        return render_template('dashboard/expression.html', 
            title="Data Ekspresi", expression=expression)

    return redirect(url_for('auth.login_admin'))

@expression.route('/dashboard/expression/<string:id>', methods=['GET'])
def get_expression(id):
    try:
        expression = Expression.query.filter_by(id_expression=int(id)).first()
        
        data = {
            'id_expression': expression.id_expression,
            'expression_name': expression.expression_name
        }
    except Exception as e:
        print('error to qurey expression')
        print(e)

    return jsonify(data)

@expression.route('/dashboard/expression/add', methods=['POST'])
def add_expression():
    if request.method == 'POST':
        try:
            expression = Expression(expression_name=request.form.get('name'))
            db.session.add(expression)
            db.session.commit()
        except Exception as e:
            print('error to add expression')
            print(e)

        return redirect(url_for('expression.index'))

    return redirect(url_for('expression.index'))

@expression.route('/dashboard/expression/edit/<int:id>', methods=['POST'])
def edit_expression(id):
    if request.method == 'POST':
        try:
            expression = Expression.query.filter_by(id_expression=id).first()
            expression.expression_name = request.form.get('name')
            db.session.commit()
        except Exception as e:
            print('error to update expression')
            print(e)

        return redirect(url_for('expression.index'))

    return redirect(url_for('expression.index'))

@expression.route('/dashboard/expression/delete/<int:id>')
def delete_expression(id):
    try:
        expression = Expression.query.filter_by(id_expression=id).first()
        db.session.delete(expression)
        db.session.commit()
    except Exception as e:
        print('error to delete expression')
        print(e)
    
    return jsonify('')