from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

class Settings(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = Config.DATABASE_INTERFACE_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False