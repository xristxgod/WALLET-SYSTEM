from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "main.login_page"
login_manager.login_message_category = "info"

def init_app():
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "main.login_page"
    login_manager.login_message_category = "info"

    return app