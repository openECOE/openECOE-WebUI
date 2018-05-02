from flask import render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm
from potion_client import Client
from potion_client.auth import HTTPBearerAuth
from potion_client.exceptions import ItemNotFound


@bp.route('/', methods=['GET'])
@login_required
def home():

    client = current_user.api_client
    ecoe = client.Ecoe.instances()

    return render_template('admin.html', ecoes=ecoe)


@bp.route('/auth', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)
        )
        return redirect(url_for('index'))
    return render_template('auth.html',  title='Sign In', form=form)

@bp.route('/eval', methods=['GET'])
def eval():
    # stations = client.Station.instances()
    # for sta in stations:
    #     print("{} yee")

    return render_template('evaluation.html', title='Evaluación', ecoeName='ECOE 1', stations=["Sta 1", "Sta 2", "Sta 3", "Sta 4", "Sta 5"])
