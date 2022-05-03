import logging

from flask import Flask, request, redirect
from flask_migrate import Migrate

from src import settings,  models

app = Flask(__name__)
migrate = Migrate(app, settings.db)

def clear_trailing():
    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])

def init_app(config=settings.Settings):
    global app
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    settings.db.init_app(app)
    app.before_request(clear_trailing)
    app.logger.setLevel(logging.INFO)
    return app