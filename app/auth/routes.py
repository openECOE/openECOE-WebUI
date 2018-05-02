from flask import render_template, redirect, url_for, flash, request, current_app, g
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, UserMixin
from flask_babel import _
from app.auth import bp
from app.auth.forms import LoginForm
from app import Client, login_manager, current_app
import requests
from requests.auth import HTTPBasicAuth
from potion_client.auth import HTTPBearerAuth


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ui_admin.home'))
    form = LoginForm()
    if form.validate_on_submit():
        response = requests.post("http://10.1.56.84:5000/auth/tokens", auth=HTTPBasicAuth(form.username.data, form.password.data))

        if response.status_code == requests.codes.ok:
            json = response.json()
            token = json['token']
            token_expiration = json['expiration']

            login_user(load_user(token), remember=form.remember_me.data)


            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('ui_admin.home')
            return redirect(next_page)

    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    pass


@login_manager.user_loader
def load_user(token):
    logged_user = UserMixin()

    logged_user.api_client = Client(current_app.config['API_ROUTE'], auth=HTTPBearerAuth(token))

    user = logged_user.api_client.User.read_me()

    logged_user.token = token
    logged_user.id = token
    logged_user.username = user.email
    logged_user.name = user.name
    logged_user.surname = user.surname


    return logged_user
