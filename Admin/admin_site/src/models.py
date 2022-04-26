import pyotp
from flask_login import UserMixin

from src.__init__ import login_manager
from src.settings import db

from config import Config

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

def is_password_correction(password: str):
    if Config.ADMIN_PASSWORD == password:
        return True
    return False

def is_google_auth_code_correction(code: str):
    if pyotp.TOTP(Config.ADMIN_GOOGLE_AUTH_SECRET_KEY).now() == code:
        return True
    return False


class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    wallets = db.relationship('WalletModel', backref='user', lazy=True)
    transactions = db.relationship('WalletTransactionModel', backref='user', lazy=True)

class WalletModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False, unique=True)
    private_key = db.Column(db.String(256), nullable=False, unique=True)
    public_key = db.Column(db.String(256), nullable=False, unique=True)
    passphrase = db.Column(db.String(256), nullable=False)
    mnemonic_phrase = db.Column(db.String(256), nullable=False, unique=True)
    accounts = db.Column(db.JSON(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

class WalletTransactionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    time = db.Column(db.Integer)
    transaction_hash = db.Column(db.String(256), nullable=False, unique=True)
    fee = db.Column(db.DECIMAL(), nullable=True)
    amount = db.Column(db.DECIMAL(), nullable=False)
    senders = db.Column(db.JSON(), nullable=True)
    recipients = db.Column(db.JSON(), nullable=True)
    token = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

class TokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False, unique=True)
    decimals = db.Column(db.Integer)
    token_info = db.Column(db.JSON(), nullable=True)