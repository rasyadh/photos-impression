import datetime
from project import app
from project.models import db
import project.models.expression
import project.models.result_detection

class DetectionSecond(db.Model):
    __tablename__ = 'detection_second'

    id_detection_second = db.Column(db.Integer, primary_key=True)
    id_result_detection = db.Column(db.Integer, db.ForeignKey('result_detection.id_result_detection'))
    id_photo = db.Column(db.Integer, db.ForeignKey('photos.id_photo'))
    time_detected = db.Column(db.Float, nullable=False)
    result_expression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))

    def __repr__(self):
        return '<Detection Second {0}>'.format(self.id_detection_second)