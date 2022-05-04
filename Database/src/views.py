import json

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from src.forms import LoginForm, GoogleAuthForm
from src.forms import RemoveForm, AddTokenForm, UpdateForm

from src.models import UserModel, WalletTransactionModel, WalletModel, TokenModel
from src.models import is_password_correction, is_google_auth_code_correction

from src.settings import db

from src.services.helper import Helper
from config import logger

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

@app.route("/checking-code/<hash_info>", methods=['GET', 'POST'])
def checking_code_page(hash_info: str):
    user = UserModel.query.filter_by(id=json.loads(bytes.fromhex(hash_info).decode("utf-8")).get("id")).first()
    if not user.is_admin:
        flash('You are not an admin!', category='danger')
        return redirect(url_for("main.main_page"))
    form = GoogleAuthForm()
    if form.validate_on_submit():
        if is_google_auth_code_correction(code=form.code.data):
            login_user(user)
            return redirect(url_for('main.index_page'))
        else:
            flash("The code didn't fit. Try again", "danger")
            return redirect(url_for('main.checking_code_page', hash_info=hash_info, _external=True))
    return render_template(
        "checking_code.html",
        form=form
    )

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("main.login_page"))

# <<<==================================>>> Main pages <<<============================================================>>>

@app.route('/')
@login_required
def index_page():
    return render_template(
        "home.html",
        users_count=UserModel.query.count(),
        users=UserModel.query.order_by("id"),
        wallets_count=WalletModel.query.count(),
        wallets=WalletModel.query.order_by("id"),
        transactions_count=WalletTransactionModel.query.count(),
        transactions=WalletTransactionModel.query.order_by("id"),
        tokens_count=TokenModel.query.count(),
        tokens=TokenModel.query.order_by("id"),
    )

# <<<==================================>>> Token pages <<<============================================================>>>

@app.route("/tokens", methods=['GET', 'POST'])
def token_page():
    add_form = AddTokenForm()
    remove_form = RemoveForm()
    upd_form = UpdateForm()
    if request.method == "POST":
        if add_form.validate_on_submit():
            if request.form.get('added_token') is not None:
                if add_form.token_info.data is not None:
                    try:
                        json.loads(add_form.token_info.data)
                    except ValueError:
                        flash('The "Token info" field must be JSON. Example: {"info": "...", "info2": "..."}', category='danger')
                        return redirect(url_for("main.token_page"))
                try:
                    create_token = TokenModel(
                        network=add_form.network.data,
                        token=add_form.token.data,
                        address=add_form.address.data,
                        decimals=add_form.decimals.data,
                        token_info=add_form.token_info.data
                    )
                    db.session.add(create_token)
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    logger.error(f"ERROR: {error}")
                    flash("Something went wrong...")
            return redirect(url_for("main.token_page"))

        if remove_form.validate_on_submit():
            remove_token = request.form.get("remove_token")

        if upd_form.validate_on_submit():
            update_token = request.form.get("update_token")

    return render_template(
        "token.html",
        tokens=Helper.get_all_tokens(TokenModel.query.order_by("id")),
        add_form=add_form,
        remove_form=remove_form,
        upg_form=upd_form
    )