import os

from flask import Flask
import config

APP_SETTINGS = config.DevelopmentConfig

app = Flask(__name__)

#use this for windows
app.config.from_object(APP_SETTINGS)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + '\static\image\photos'

#use this for linux
#app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run(threaded=True)

from project import core
from project import views
from project import models