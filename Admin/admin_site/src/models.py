from flask_login import UserMixin

from src.__init__ import login_manager
from src.settings import db

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False, unique=True)
    private_key = db.Column(db.String(256), nullable=False, unique=True)
    public_key = db.Column(db.String(256), nullable=False, unique=True)
    passphrase = db.Column(db.String(256), nullable=False)
    mnemonic_phrase = db.Column(db.String(256), nullable=False, unique=True)
    accounts = db.Column(db.JSON(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))