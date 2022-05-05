from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired

# <<<==================================>>> Authorization forms <<<=============================================>>>

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class GoogleAuthForm(FlaskForm):
    code = StringField(label='Code from the GoogleAuthenticator app:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# <<<==================================>>> Remove And Update <<<=====================================================>>>

class RemoveForm(FlaskForm):
    submit = SubmitField(label='Remove')

class UpdateForm(FlaskForm):
    submit = SubmitField(label='Update')

# <<<==================================>>> User model form <<<=======================================================>>>

class AddUserForm(FlaskForm):
    chat_id = IntegerField(label='Chat id: ', validators=[DataRequired()])
    username = StringField(label='Username: ', validators=[DataRequired()], description="Must start with `@'")
    is_admin = BooleanField(label="Will he be an admin: ", validators=[DataRequired()])
    submit = SubmitField(label='Add')

# <<<==================================>>> Token form <<<============================================================>>>

class AddTokenForm(FlaskForm):
    network = StringField(label='Network: ', validators=[DataRequired()])
    token = StringField(label='Token symbol: ', validators=[DataRequired()])
    address = StringField(label='Smart contract address: ', validators=[DataRequired()])
    decimals = IntegerField(label='Decimals: ', validators=[DataRequired()], default=0)
    token_info = StringField(label='Token info: ', validators=[DataRequired()], default="{}")
    submit = SubmitField(label='Add')

# <<<==================================>>> Wallet form <<<===========================================================>>>

class AddWalletForm(FlaskForm):
    network = SelectField(label='Network: ', validators=[DataRequired()])
    address = StringField(label='Wallet address: ', validators=[DataRequired()])
    private_key = StringField(label='Wallet private key: ', validators=[DataRequired()])
    public_key = StringField(label='Wallet public key: ', validators=[DataRequired()])
    passphrase = StringField(label='Wallet passphrase: ', validators=[DataRequired()])
    mnemonic_phrase = StringField(label='Wallet mnemonic phrase: ', validators=[DataRequired()])
    user_id = SelectField(label="The wallet belongs to the user: ", validators=[DataRequired()])
    submit = SubmitField(label='Add')

# <<<==================================>>> Wallet transaction form <<<===============================================>>>

class AddWalletTransactionForm(FlaskForm):
    network = SelectField(label='Network: ', validators=[DataRequired()])
    time = SelectField(label="Select the transaction time: ", validators=[DataRequired()])
    transaction_hash = StringField(label='Transaction hash: ', validators=[DataRequired()])
    fee = DecimalField(label='Transaction fee: ', validators=[DataRequired()])
    amount = DecimalField(label='Transaction amount: ', validators=[DataRequired()])
    senders = StringField(label='Sender/s: ', validators=[DataRequired()], default=None)
    recipients = StringField(label='Recipient/s: ', validators=[DataRequired()], default=None)
    token = SelectField(label='Token symbol: ', validators=[DataRequired()])
    status = BooleanField(label="Status: ", validators=[DataRequired()])
    user_id = SelectField(label="The wallet belongs to the user: ", validators=[DataRequired()])
    submit = SubmitField(label='Add')