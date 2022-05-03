from flask import Flask
from flask_migrate import Migrate

from src import settings,  models

app = Flask(__name__)
migrate = Migrate(app, settings.db)

def init_app(config=settings.Settings):
    global app
    app.config.from_object(config)
    settings.db.init_app(app)
    return app