import datetime
from project.core import db
from project import app

class Expression(db.Model):
    __tablename__ = 'expression'

    # Expression (1 = netral, 2 = bahagia, 3 = sedih, 4 = terkejut)
    id_expression = db.Column(db.Integer, primary_key=True) 
    expression_name = db.Column(db.String(20), nullable=False)
    expression_feature = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<expression {0}>'.format(self.expression_name)

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

class ResultDetection(db.Model):
    __tablename__ = 'result_detection'

    # category photos (1: random, 2: bahagia, 3: sedih, 4: terkejut)
    id_result_detection = db.Column(db.Integer, primary_key=True)
    category_photos = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def get_id_result_detection(self):
        return self.id
    
    def __repr__(self):
        return '<ResultDetection {0}>'.format(self.id_result_detection)

class Detection(db.Model):
    __tablename__ = 'detection'

    id_detection = db.Column(db.Integer, primary_key=True)
    id_result_detection = db.Column(db.Integer, db.ForeignKey('result_detection.id_result_detection'))
    id_photo = db.Column(db.Integer, db.ForeignKey('photos.id_photo'))
    time_detected = db.Column(db.Float, nullable=False)
    initial_expression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))
    result_expression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))

    def __repr__(self):
        return '<Detection {0}>'.format(self.id_detection)

class Admin(db.Model):
    __tablename__ = 'admin'

    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Admin {0}>'.format(self.username)