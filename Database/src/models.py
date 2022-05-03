from src.settings import db

class UserModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class WalletMode():
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False, unique=True)
    private_key = db.Column(db.String(256), nullable=False, unique=True)
    public_key = db.Column(db.String(256), nullable=False, unique=True)
    passphrase = db.Column(db.String(256), nullable=False)
    mnemonic_phrase = db.Column(db.String(256), nullable=False, unique=True)
    accounts = db.Column(db.JSON, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

class WalletTransactionModel():
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    time = db.Column(db.Integer)
    transaction_hash = db.Column(db.String(256), nullable=False, unique=True)
    fee = db.Column(db.DECIMAL, nullable=True, default=0)
    amount = db.Column(db.DECIMAL, nullable=False, default=0)
    senders = db.Column(db.JSON, nullable=True)
    recipients = db.Column(db.JSON, nullable=True)
    token = db.Column(db.String(256), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

class TokenModel():

    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False, unique=True)
    decimals = db.Column(db.Integer)
    token_info = db.Column(db.JSON, nullable=True)