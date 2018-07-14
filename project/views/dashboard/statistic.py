import json
from operator import itemgetter
from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for
)
from project.globals import PHOTO_EXPRESSION, PHOTOS_SEQUENCE
from project.models import db

statistic = Blueprint('statistic', __name__)

@statistic.route('/dashboard/statistic/')
def index():
    if session.get('loggedin_admin'):
        try:
            result_trend = db.engine.execute("SELECT d.id_photo, p.photo_url, d.result_expression, COUNT(d.id_photo) FROM detection d, photos p WHERE d.id_photo = p.id_photo GROUP BY d.id_photo, d.result_expression")

            trend = create_trend(result_trend)

            head_table = []
            for photo in PHOTOS_SEQUENCE:
                head_table.append(photo['id_photo'])

            result_table = db.engine.execute("SELECT u.username, dp.id_photo, dp.result_expression FROM user u, result_detection rd, detection_photo dp WHERE u.id_user = rd.id_user and rd.id_result_detection = dp.id_result_detection")

            table, total = create_table(result_table)
        except Exception as e:
            print(e)

        return render_template('dashboard/statistic.html',
            title='Statistik', trend=trend, htable=head_table, table=table, total=total)

    return redirect(url_for('auth.login_admin'))

def create_trend(result):
    expression = { 1: 'Bahagia', 2: 'Sedih', 3: 'Terkejut' }
    data = {
            "netral": [],
            "bahagia": [],
            "sedih": [],
            "terkejut": []
    }

    for res in result:
        temp = {
            "id_photo": res[0],
            "photo_url": res[1],
            "result_expression": expression[res[2]],
            "occurance": res[3]
        }

        if res[2] == 0:
            data["netral"].append(temp)
        elif res[2] == 1:
            data["bahagia"].append(temp)
        elif res[2] == 2:
            data["sedih"].append(temp)
        elif res[2] == 3:
            data["terkejut"].append(temp)
        temp = {}

    trend = {
        "netral": sorted(data["netral"], key=itemgetter('occurance'), reverse=True)[:5],
        "bahagia": sorted(data["bahagia"], key=itemgetter('occurance'), reverse=True)[:5],
        "sedih": sorted(data["sedih"], key=itemgetter('occurance'), reverse=True)[:5],
        "terkejut": sorted(data["terkejut"], key=itemgetter('occurance'), reverse=True)[:5]
    }

    return trend

def create_table(result):
    data, table, tfoot = {}, [], []
    expr_photo = PHOTO_EXPRESSION.copy()

    for res in result:
        if res.username not in data:
            data[res.username] = [{
                'id_photo': res.id_photo,
                'expression': res.result_expression
            }]
        else:
            data[res.username].append({
                'id_photo': res.id_photo,
                'expression': res.result_expression
            })

    for key, value in data.items():
        temp = {
            'username': key,
            'data': [],
            'error': 0,
            'netral': 0
        }
        for val in value:
            if val['expression'] == 0:
                temp['data'].append(0)
                temp['netral'] += 1
            elif val['id_photo'] in expr_photo[str(val['expression'])]:
                temp['data'].append(1)
            else:
                temp['data'].append(-1)
                temp['error'] += 1
        table.append(temp)

    total = [0] * 30
    for user in table:
        for i in range(len(user['data'])):
            if user['data'][i] == -1:
                total[i] += 1
            else:
                total[i] += 0

    return table, total
