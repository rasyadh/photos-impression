from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from project.models.photos import Photos

photos = Blueprint('photos', __name__)

@photos.route('/photos/')
def index():
    if session.get('loggedin'):    
        try:
            photos = Photos.query.all()
            impresi = { 2: 'bahagia', 3: 'sedih', 4: 'terkejut' }
            result, data = [], {}

            for p in photos:
                if p.comment_impression in impresi:
                    p.comment_impression = impresi[p.comment_impression]

                data = {
                    'id_photo': p.id_photo,
                    'photo_name': p.photo_name,
                    'photo_url': p.photo_url,
                    'source_url': p.source_url,
                    'comment_impression': p.comment_impression
                }

                result.append(data)
                data = {}
        except Exception as e:
            print('error query photos')
            print(e)

        return render_template('photos/photos.html', 
            title="Foto Percobaan", photos=result)
    else:
        return redirect(url_for('auth.login'))