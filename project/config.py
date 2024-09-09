import os.path
from project import app

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(basedir, 'userdb.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# General Config
ENVIRONMENT = "development"
FLASK_APP = "flask-app1"
FLASK_DEBUG = True

