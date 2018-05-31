import datetime
from project import app
from project.models import db

# Id Expression 
# 1 = netral, 2 = bahagia, 3 = sedih, 4 = terkejut
class Expression(db.Model):
    __tablename__ = 'expression'

    id_expression = db.Column(db.Integer, primary_key=True) 
    expression_name = db.Column(db.String(20), nullable=False)
    expression_feature = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<expression {0}>'.format(self.expression_name)