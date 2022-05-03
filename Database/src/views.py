import json

from flask import Blueprint, render_template, redirect, url_for, flash

from src.forms import LoginForm, GoogleAuthForm
from src.models import UserModel
from src.models import is_password_correction

app = Blueprint("main", __name__)

# <<<==================================>>> Authorization pages <<<===================================================>>>

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = UserModel.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.is_admin and is_password_correction(password=form.password.data):
            return redirect(url_for('main.checking_code_page', hash_info=json.dumps({
                "id": attempted_user.id,
                "username": attempted_user.username,
            }).encode("utf-8").hex(), _external=True))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template(
        "login.html",
        form=form
    )