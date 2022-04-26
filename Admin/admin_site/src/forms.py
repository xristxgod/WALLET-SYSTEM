from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class GoogleAuthForm(FlaskForm):
    code = StringField(label='Code from the GoogleAuthenticator app:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')