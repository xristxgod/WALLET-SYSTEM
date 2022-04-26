from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from src.__init__ import app
from config import Config

db = SQLAlchemy()
migrate = Migrate(app, db)

app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL

def db_setup():
    db.create_all()
    pass

def close_db(e=None):
    pass

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    db_setup()