import logging

from flask import Flask, request, redirect
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "main.login_page"
login_manager.login_message_category = "info"

def clear_trailing():
    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])

def init_app():
    from src import settings, views, jobs
    app.url_map.strict_slashes = False
    settings.init_app(app)
    jobs.register_scheduler(app)
    app.before_request(clear_trailing)
    app.register_blueprint(views.app)

    app.logger.setLevel(logging.INFO)

    return app