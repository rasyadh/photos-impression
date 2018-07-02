import json
from operator import itemgetter
from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for
)
from project.models import db

statistic = Blueprint('statistic', __name__)

@statistic.route('/dashboard/statistic/')
def index():
    expression = { 1: 'Bahagia', 2: 'Sedih', 3: 'Terkejut' }
    if session.get('loggedin_admin'):
        result = db.engine.execute("SELECT d.id_photo, p.photo_url, d.result_expression, COUNT(d.id_photo) FROM detection d, photos p WHERE d.id_photo = p.id_photo GROUP BY d.id_photo, d.result_expression")

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

        return render_template('dashboard/statistic.html',
            title='Statistik', trend=trend)

    return redirect(url_for('auth.login_admin'))