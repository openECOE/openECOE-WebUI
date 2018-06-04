from flask import render_template, flash, redirect, url_for, current_app, make_response, jsonify, json
from flask_login import login_required, current_user
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm, AddAreaForm, AddStationForm, AddStudentForm
from potion_client.exceptions import ItemNotFound
from flask import request


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET'])
@login_required
def home():
    ecoes = current_user.api_client.Ecoe.instances()
    return render_template('index.html', ecoes=ecoes)


@bp.route('/ecoe/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/info/', methods=['GET'])
@login_required
def infoEcoe(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    areas = current_user.api_client.Area.instances(where={"ecoe": ecoe})
    stations = current_user.api_client.Station.instances(where={"ecoe": ecoe})
    students = current_user.api_client.Student.instances(where={"ecoe": ecoe})

    # rounds_array = []
    # for student in students:
    #     rounds = current_user.api_client.Round.instances()
    #     rounds_array.append(rounds)


    return render_template('info-ecoe.html', ecoe=ecoe, id_ecoe=id_ecoe, areas_length=areas._total_count, stations=stations, students_length=students._total_count)



@bp.route('/ecoe/<id_ecoe>/area/', methods=['GET', 'POST', 'PATCH'])
@login_required
def areas(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)

    formAdd = AddAreaForm(request.form)
    if request.method == 'POST' and formAdd.validate():
        new_area = current_user.api_client.Area()
        new_area.name = formAdd.name.data
        new_area.ecoe = ecoe

        try:
            new_area.save()
            flash('{} created'.format(new_area.name))
        except:
            flash('Nombre de area duplicado')

    areas = current_user.api_client.Area.instances(where={"ecoe": ecoe})
    return render_template('areas.html', areas=areas, id_ecoe=id_ecoe, formAdd=formAdd)

@bp.route('/<model>/<id_item>/delete/', methods=['DELETE'])
@login_required
def delete_item(model, id_item):
    if request.method == 'DELETE':
        # id_item = request.args.get('id')
        item = None

        if model == 'area':
            item = current_user.api_client.Area(id_item)
        elif model == 'station':
            item = current_user.api_client.Station(id_item)

        try:
            item.destroy()
            return jsonify({'status': 204})
        except:
            flash('Error al borrar')
            print('Error')
            return jsonify({'status': 404})

@bp.route('/<model>/<id_item>/edit', methods=['PATCH'])
@login_required
def edit_item(model, id_item):
    if request.method == 'PATCH':
        new_name = request.args.get('name') or request.args.get('amp;name')

        if id_item and new_name:
            item = None

            if model == 'area':
                item = current_user.api_client.Area(id_item)
            elif model == 'station':
                item = current_user.api_client.Station(id_item)

            try:
                item.update(name=new_name)
                return jsonify({'status': 200})
            except:
                flash('Error al modificar')
                print('Error')
                return jsonify({'status': 404})

@bp.route('/ecoe/<int:id_ecoe>/stations/', methods=['GET', 'POST'])
@login_required
def stations(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)

    formAdd = AddStationForm(request.form)
    if request.method == 'POST' and formAdd.validate():
        new_station = current_user.api_client.Station()
        new_station.name = formAdd.name.data
        new_station.ecoe = ecoe

        try:
            new_station.save()
            flash('{} created'.format(new_station.name))
        except:
            flash('Nombre de estación duplicado')

    stations = current_user.api_client.Station.instances(where={"ecoe": ecoe})
    return render_template('stations.html', stations=stations, id_ecoe=id_ecoe, formAdd=formAdd)

@bp.route('ecoe/<id_ecoe>/station/<id_station>/qblocks', methods=['GET'])
@login_required
def get_qblocks(id_ecoe, id_station):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    areas = current_user.api_client.Area.instances(where={"ecoe": ecoe})
    station = current_user.api_client.Station(id_station)

    qblocks = station.qblocks()
    qblocks_array = []
    for qblock in qblocks:
        qblocks_array.append({'qblock': qblock, 'questions': qblock.questions()})

    return render_template('station-qblocks.html', station=station, qblocks=qblocks_array, areas=areas)

@bp.route('question/<id_question>/', methods=['GET'])
@login_required
def get_options(id_question):
    question = current_user.api_client.Question(id_question)
    options = current_user.api_client.Option.instances(where={"question": question})

    return render_template('question-options.html', options=options)

# TODO: falta relacionar chronos con ecoes
@bp.route('/ecoe/<int:id_ecoe>/chronometers/', methods=['GET', 'POST'])
@login_required
def chronometers(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    # form = AddChronometerForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     new_chrono = current_user.api_client.Area()
    #     new_chrono.name = form.name.data
    #     new_chrono.ecoe = ecoe
    #
    #     try:
    #         new_chrono.save()
    #         flash('{} created'.format(new_chrono.name))
    #     except:
    #         flash('Nombre de area duplicado')

    # chronometer = current_user.api_client.Chronometer.instances(where={"ecoe": ecoe})
    return render_template('chronometers.html', chronometers=[{'name': 'Chrono 1'},{'name': 'Chrono 2'},{'name': 'Chrono 3'}], id_ecoe=id_ecoe)

@bp.route('/ecoe/<int:id_ecoe>/students/', methods=['GET', 'POST'])
@login_required
def students(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)

    form = AddStudentForm(request.form)
    if request.method == 'POST' and form.validate():
        new_student = current_user.api_client.Student()
        new_student.name = form.name.data
        new_student.dni = form.dni.data
        new_student.ecoe = ecoe

        try:
            new_student.save()
            flash('Student {} created'.format(new_student.name))
        except:
            flash('Estudiante duplicado')

    students = current_user.api_client.Student.instances(where={"ecoe": ecoe})
    return render_template('students.html', students=students, id_ecoe=id_ecoe, form=form)

# TODO: obtener grupos a partir de la Ecoe
@bp.route('/ecoe/<int:id_ecoe>/groups/', methods=['GET', 'POST'])
@login_required
def groups(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    groups = current_user.api_client.Group.instances(where={"ecoe": ecoe})
    return render_template('groups.html', groups=groups, id_ecoe=id_ecoe)

# @bp.route('/statistics', methods=['GET', 'POST'])
# @login_required
# def statistics(id_ecoe):
#     ecoe = current_user.api_client.Ecoe(id_ecoe)
#     student = current_user.api_client.Student.instances(where={"ecoe": ecoe})
#     return render_template('statistics.html', students=student, id_ecoe=id_ecoe)


@bp.route('/eval/', methods=['GET'])
@login_required
def eval():
    # stations = current_user.api_client.Station.instances()
    # for sta in stations:
    #     print("{} yee")

    return render_template('evaluation.html', title='Evaluación', ecoeName='ECOE 1', stations=["Sta 1", "Sta 2", "Sta 3", "Sta 4", "Sta 5"])
