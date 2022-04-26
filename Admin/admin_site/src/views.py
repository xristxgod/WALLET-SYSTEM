import json

from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user

from src.forms import LoginForm, GoogleAuthForm
from src.models import UserModel, is_password_correction, is_google_auth_code_correction

from src.services.events import Events
from src.services.favorites import FavoritesUsers

from config import Config

app = Blueprint("main", __name__)
favorites = FavoritesUsers()

# <<<========================================>>> Authorization <<<===================================================>>>

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = UserModel.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.is_admin and is_password_correction(password=form.password.data):
            return redirect(url_for('main.checking_code', hash_info=json.dumps({
                "id": attempted_user.id,
                "username": attempted_user.username,
            }).encode("utf-8").hex(), _external=True))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template(
        "login.html",
        form=form
    )

@app.route("/checking-code/<hash_info>", methods=['GET', 'POST'])
def checking_code(hash_info: str):
    user = UserModel.query.filter_by(id=json.loads(bytes.fromhex(hash_info).decode("utf-8")).get("id")).first()
    if not user.is_admin:
        flash('You are not an admin!', category='danger')
        return redirect(url_for("main.login_page"))
    form = GoogleAuthForm()
    if form.validate_on_submit():
        if is_google_auth_code_correction(code=form.code.data):
            login_user(user)
            return redirect(url_for('main.index_page'))
        else:
            flash("The code didn't fit. Try again", "danger")
            return redirect(url_for('main.checking_code', hash_info=hash_info, _external=True))
    return render_template(
        "checking_code.html",
        form=form
    )