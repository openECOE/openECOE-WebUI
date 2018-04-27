from flask import render_template, flash, redirect, url_for, current_app
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm
from potion_client import Client
from potion_client.auth import HTTPBearerAuth
from potion_client.exceptions import ItemNotFound
from config import Config



@bp.route('/', methods=['GET'])
def home():

    api_route = Config.API_ROUTE

    client = Client(api_route)
    ecoe = client.Ecoe.instances()

    return render_template('admin.html', ecoes=ecoe)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)
        )
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)

@bp.route('/eval', methods=['GET'])
def eval():
    # stations = client.Station.instances()
    # for sta in stations:
    #     print("{} yee")

    return render_template('evaluation.html', title='Evaluación', ecoeName='ECOE 1', stations=["Sta 1", "Sta 2", "Sta 3", "Sta 4", "Sta 5"])
