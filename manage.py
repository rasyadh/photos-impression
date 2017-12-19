import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app
from project.core import db

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

@manager.command
def createdb():
	db.create_all()

if __name__ == '__main__':
	manager.run()