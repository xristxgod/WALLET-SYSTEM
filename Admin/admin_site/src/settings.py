from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

class Settings(object):
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True