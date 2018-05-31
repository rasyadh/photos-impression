import datetime
from project import app
from project.models import db
import project.models.expression

class Photos(db.Model):
    __tablename__ = 'photos'

    id_photo = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False, unique=True)
    source_url = db.Column(db.String(255), nullable=True, unique=True)
    comment_impression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    
    def get_id_photo(self):
        return self.id_photo

    def __repr__(self):
        return '<Photos {0}>'.format(self.photo_name)