from flask_script import Manager
from flask_migrate import (
	Migrate,
	MigrateCommand
)
from project import app
from project.models import *

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def createdb():
	db.create_all()

@manager.command
def dropdb():
	db.drop_all()

@manager.command
def createadmin():
	admin = Admin(username='admin', password='admin123')
	db.session.add(admin)
	db.session.commit()

if __name__ == '__main__':
	manager.run()