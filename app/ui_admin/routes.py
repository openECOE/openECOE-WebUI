from flask import render_template, flash, redirect, url_for, current_app
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm, AddAreaForm
from potion_client import Client
from potion_client.auth import HTTPBearerAuth
from potion_client.exceptions import ItemNotFound
from flask import request
from config import Config

api_route = Config.API_ROUTE
client = Client(api_route)

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    ecoe = client.Ecoe.instances()
    return render_template('index.html', ecoes=ecoe)

@bp.route('/info-ecoe/', methods=['GET'])
@bp.route('/info-ecoe/<int:id_ecoe>', methods=['GET'])
def infoEcoe(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    return render_template('info-ecoe.html', ecoe=ecoe, id_ecoe=id_ecoe)

@bp.route('/ecoe/<int:id_ecoe>/areas', methods=['GET', 'POST'])
def areas(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    area = client.Area.instances(where={"ecoe":ecoe})

    form = AddAreaForm(csrf_enabled=False)
    if form.validate_on_submit():
        flash('Add area {} requested'.format(form.name))
        return redirect(url_for('index'))

    return render_template('areas.html', areas=area, id_ecoe=id_ecoe, form=form)

@bp.route('/ecoe/<int:id_ecoe>/stations', methods=['GET', 'POST'])
def stations(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    station = client.Station.instances(where={"ecoe": ecoe})
    return render_template('stations.html', stations=station, id_ecoe=id_ecoe)

# TODO: falta relacionar chronos con ecoes
@bp.route('/ecoe/<int:id_ecoe>/chronometers', methods=['GET', 'POST'])
def chronometers(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    # chronometer = client.Chronometer.instances(where={"ecoe": ecoe})
    return render_template('chronometers.html', chronometers=[{'name': 'Chrono 1'},{'name': 'Chrono 2'},{'name': 'Chrono 3'}], id_ecoe=id_ecoe)

@bp.route('/ecoe/<int:id_ecoe>/students', methods=['GET', 'POST'])
def students(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    student = client.Student.instances(where={"ecoe": ecoe})
    return render_template('students.html', students=student, id_ecoe=id_ecoe)

# TODO: obtener grupos a partir de la Ecoe
@bp.route('/ecoe/<int:id_ecoe>/groups', methods=['GET', 'POST'])
def groups(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    group = client.Group.instances(where={"ecoe": ecoe})
    return render_template('groups.html', groups=group, id_ecoe=id_ecoe)

# @bp.route('/statistics', methods=['GET', 'POST'])
# def statistics(id_ecoe):
#     ecoe = client.Ecoe(id_ecoe)
#     student = client.Student.instances(where={"ecoe": ecoe})
#     return render_template('statistics.html', students=student, id_ecoe=id_ecoe)


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
