import datetime
from project import app
from project.models import db

class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User {0}>'.format(self.username)