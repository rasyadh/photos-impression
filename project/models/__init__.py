from project import app
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy(app)