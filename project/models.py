import datetime
from project.core import db
from project import app

class Photos(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)
    impression = db.Column(db.String(1), nullable=False) # H=happy S=Sad N=Netral T=Terkejut
    created_at = db.Column(db.DateTime)

    def __init__(self, name=None, url=None, impression=None):
        self.name = name
        self.url = url
        self.impression = impression
        self.created_at = datetime.date.today()
        
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Photos {0}>'.format(self.name)

class FacialExpression(db.Model):
    __tablename__ = 'facial_expression'

    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(10), nullable=False)

    def __init__(self, expression=None):
        self.expression = expression

    def __repr__(self):
        return '<FacialExpression {0}'.format(self.expression)