import logging
import os.path
import sys
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile("config.py")
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'userdb.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# General Config
ENVIRONMENT = "development"
FLASK_APP = "flask-app1"
FLASK_DEBUG = True


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "my_app.log"


def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler


def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler


def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   if app.config['ENVIRONMENT'] == 'production':
      logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent

   logger.propagate = False
   return logger


# logging.basicConfig(filename='record.log', level=logging.DEBUG,
#                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('Error')

db = SQLAlchemy(app)
my_logger = get_logger(__name__)

import project.views
import project.config
