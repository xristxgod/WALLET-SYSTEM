import logging

from flask import Flask, redirect, request
from flask_migrate import Migrate
from flask_login import LoginManager

from src import settings, models, views
from src.api import endpoints, system

app = Flask(__name__)
migrate = Migrate(app, settings.db)
login_manager = LoginManager(app)
login_manager.login_view = "main.login_page"
login_manager.login_message_category = "info"

def clear_trailing():
    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])

@login_manager.user_loader
def load_user(user_id):
    return models.UserModel.query.get(int(user_id))

def init_app(config=settings.Settings):
    global app
    app.config.from_object(config)
    # View
    app.register_blueprint(views.app)
    # Api blueprint
    app.register_blueprint(endpoints.app)
    app.register_blueprint(system.app)
    app.before_request(clear_trailing)
    settings.db.init_app(app)
    app.logger.setLevel(logging.INFO)
    return app