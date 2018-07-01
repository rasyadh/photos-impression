import datetime
from project import app
from project.models import db
import project.models.user

# Category Photos 
# 1: random, 2: bahagia, 3: sedih, 4: terkejut

class ResultDetection(db.Model):
    __tablename__ = 'result_detection'

    id_result_detection = db.Column(db.Integer, primary_key=True)
    category_photos = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))

    def get_id_result_detection(self):
        return self.id
    
    def __repr__(self):
        return '<ResultDetection {0}>'.format(self.id_result_detection)