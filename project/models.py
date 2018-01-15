import datetime
from project.core import db
from project import app

class Expression(db.Model):
    __tablename__ = 'expression'

    # Expression (1 = netral, 2 = senang, 3 = sedih, 4 = terkejut)
    id_expression = db.Column(db.Integer, primary_key=True) 
    expression_name = db.Column(db.String(20), nullable=False)
    expression_feature = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, expression_name=None):
        self.expression_name = expression_name

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

    def __init__(self, photo_name=None, photo_url=None, source_url=None, comment_impression=None):
        self.photo_name = photo_name
        self.photo_url = photo_url
        self.source_url = source_url
        self.comment_impression = comment_impression
    
    def get_id_photo(self):
        return self.id_photo

    def __repr__(self):
        return '<Photos {0}>'.format(self.photo_name)

class ResultDetection(db.Model):
    __tablename__ = 'result_detection'

    id_result_detection = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def get_id_result_detection(self):
        return self.id
    
    def __repr__(self):
        return '<ResultDetection {0}'.format(self.id_result_detection)

class Detection(db.Model):
    __tablename__ = 'detection'

    id_detection = db.Column(db.Integer, primary_key=True)
    id_result_detection = db.Column(db.Integer, db.ForeignKey('result_detection.id_result_detection'))
    id_photo = db.Column(db.Integer, db.ForeignKey('photos.id_photo'))
    initial_expression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))
    result_expression = db.Column(db.Integer, db.ForeignKey('expression.id_expression'))

    def __init__(self, id_result_detection=None, id_photo=None, initial_expression=None, result_expression=None):
        self.id_result_detection = id_result_detection
        self.id_photo = id_photo
        self.initial_expression = initial_expression
        self.result_expression = result_expression

    def __repr__(self):
        return '<Detection {0}'.format(self.id_detection)

class Admin(db.Model):
    __tablename__ = 'admin'

    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Admin {0}>'.format(self.username)