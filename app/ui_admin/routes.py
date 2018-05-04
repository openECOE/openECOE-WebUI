from flask import render_template, flash, redirect, url_for, current_app
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm, AddAreaForm, AddStudentForm
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
    ecoes = client.Ecoe.instances()
    return render_template('index.html', ecoes=ecoes)

@bp.route('/ecoe/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/info', methods=['GET'])
def infoEcoe(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    areas = client.Area.instances(where={"ecoe": ecoe})
    stations = client.Station.instances(where={"ecoe": ecoe})
    students = client.Student.instances(where={"ecoe": ecoe})

    # rounds_array = []
    # for student in students:
    #     rounds = client.Round.instances()
    #     rounds_array.append(rounds)


    return render_template('info-ecoe.html', ecoe=ecoe, id_ecoe=id_ecoe, areas_length=areas._total_count, stations=stations, students_length=students._total_count)

@bp.route('/ecoe/<int:id_ecoe>/areas', methods=['GET', 'POST'])
def areas(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    form = AddAreaForm(request.form)
    if request.method == 'POST' and form.validate():
        new_area = client.Area()
        new_area.name = form.name.data
        new_area.ecoe = ecoe

        try:
            new_area.save()
            flash('{} created'.format(new_area.name))
        except:
            flash('Nombre de area duplicado')

    areas = client.Area.instances(where={"ecoe": ecoe})
    return render_template('areas.html', areas=areas, id_ecoe=id_ecoe, form=form)

@bp.route('/ecoe/<int:id_ecoe>/stations', methods=['GET', 'POST'])
def stations(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    station = client.Station.instances(where={"ecoe": ecoe})
    return render_template('stations.html', stations=station, id_ecoe=id_ecoe)

# TODO: falta relacionar chronos con ecoes
@bp.route('/ecoe/<int:id_ecoe>/chronometers', methods=['GET', 'POST'])
def chronometers(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    # form = AddChronometerForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     new_chrono = client.Area()
    #     new_chrono.name = form.name.data
    #     new_chrono.ecoe = ecoe
    #
    #     try:
    #         new_chrono.save()
    #         flash('{} created'.format(new_chrono.name))
    #     except:
    #         flash('Nombre de area duplicado')

    # chronometer = client.Chronometer.instances(where={"ecoe": ecoe})
    return render_template('chronometers.html', chronometers=[{'name': 'Chrono 1'},{'name': 'Chrono 2'},{'name': 'Chrono 3'}], id_ecoe=id_ecoe)

@bp.route('/ecoe/<int:id_ecoe>/students', methods=['GET', 'POST'])
def students(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)

    form = AddStudentForm(request.form)
    if request.method == 'POST' and form.validate():
        new_student = client.Student()
        new_student.name = form.name.data
        new_student.dni = form.dni.data
        new_student.ecoe = ecoe

        try:
            new_student.save()
            flash('Student {} created'.format(new_student.name))
        except:
            flash('Estudiante duplicado')

    students = client.Student.instances(where={"ecoe": ecoe})
    return render_template('students.html', students=students, id_ecoe=id_ecoe, form=form)

# TODO: obtener grupos a partir de la Ecoe
@bp.route('/ecoe/<int:id_ecoe>/groups', methods=['GET', 'POST'])
def groups(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    groups = client.Group.instances(where={"ecoe": ecoe})
    return render_template('groups.html', groups=groups, id_ecoe=id_ecoe)

# @bp.route('/statistics', methods=['GET', 'POST'])
# def statistics(id_ecoe):
#     ecoe = client.Ecoe(id_ecoe)
#     student = client.Student.instances(where={"ecoe": ecoe})
#     return render_template('statistics.html', students=student, id_ecoe=id_ecoe)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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
