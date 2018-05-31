from flask import Flask
import config

APP_SETTINGS = config.DevelopmentConfig

app = Flask(__name__)

# use this for windows
app.config.from_object(APP_SETTINGS)

# use this for linux
# app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run(threaded=True)

from project.views.main import main
from project.views.expression_detection import detect
from project.views.stream_webcam import stream
from project.views.photos import photos
from project.views.detection_results import result
from project.views.auth import auth

from project.views.dashboard.main import dashboard
from project.views.dashboard.expression import expression
from project.views.dashboard.feature_extraction import extraction
from project.views.dashboard.photos_collection import dashboard_photos
from project.views.dashboard.detection_results import dashboard_results

app.register_blueprint(main)
app.register_blueprint(detect)
app.register_blueprint(stream)
app.register_blueprint(photos)
app.register_blueprint(result)
app.register_blueprint(auth)

app.register_blueprint(dashboard)
app.register_blueprint(expression)
app.register_blueprint(extraction)
app.register_blueprint(dashboard_photos)
app.register_blueprint(dashboard_results)