from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

class Settings(object):
    SECRET_KEY = "324bef6c5985f7ad7c8527d2"
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True