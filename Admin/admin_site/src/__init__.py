import logging

from flask import Flask, request, redirect
from flask_migrate import Migrate
from flask_login import LoginManager

from src import settings, views, jobs, models

app = Flask(__name__)
migrate = Migrate(app, settings.db)
login_manager = LoginManager(app)
login_manager.login_view = "main.login_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return models.UserModel.query.get(int(user_id))

def clear_trailing():
    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])

def init_app(config=settings.Settings):
    global app
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    settings.db.init_app(app)
    jobs.register_scheduler(app)
    app.before_request(clear_trailing)
    app.register_blueprint(views.app)
    app.logger.setLevel(logging.INFO)
    return app