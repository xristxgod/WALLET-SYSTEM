from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired

# <<<==================================>>> Authorization forms <<<=============================================>>>

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class GoogleAuthForm(FlaskForm):
    code = StringField(label='Code from the GoogleAuthenticator app:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# <<<==================================>>> Remove <<<================================================================>>>

class RemoveForm(FlaskForm):
    submit = SubmitField(label='Remove')

# <<<==================================>>> User model form <<<=======================================================>>>

class AddUserForm(FlaskForm):
    _id = StringField(label='Chat id: ', validators=[DataRequired()])
    username = StringField(label='Username: ', validators=[DataRequired()], description="Must start with `@'")
    is_admin = BooleanField(label="Will he be an admin?")
    submit = SubmitField(label='Add')

class UpdateUserForm(FlaskForm):
    pass

# <<<==================================>>> Token form <<<============================================================>>>

class AddTokenForm(FlaskForm):
    network = StringField(label='Network: ', validators=[DataRequired()])
    token = StringField(label='Token symbol: ', validators=[DataRequired()])
    address = StringField(label='Smart contract address: ', validators=[DataRequired()])
    decimals = IntegerField(label='Decimals: ', validators=[DataRequired()], default=0)
    token_info = StringField(label='Token info: ', validators=[DataRequired()], default=None)

class UpdateTokenForm(FlaskForm):
    pass

# <<<==================================>>> Token form <<<============================================================>>>