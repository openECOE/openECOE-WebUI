from flask import render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.ui_evaluation import bp
from potion_client.exceptions import ItemNotFound
from flask import request

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    ecoe = current_user.api_client.Ecoe.instances()
    return render_template('index.html', title='Home',  ecoes=ecoe)


@bp.route('/evaluacion', methods=['GET'])
@bp.route('/evaluacion/<int:id_ecoe>/<int:id_station>', methods=['GET'])
@login_required
def evaluacion(id_ecoe, id_station):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    station = current_user.api_client.Station(id_station)
    qblocks = station.qblocks()

    questions_array = []
    for qblock in qblocks:
        questions = qblock.questions()
        for question in questions:
            options =  current_user.api_client.Option.instances(where = {"question": question})
            questions_array.append({'question': question,  'options': options})

    return render_template('evaluacion.html', ecoe=ecoe, station = station, qblock=qblocks, questions=questions_array)

@bp.route('/evaladmin/', methods=['GET'])
@bp.route('/evaladmin/<int:id_ecoe>/', methods=['GET'])
@login_required
def evaladmin(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    station = current_user.api_client.Station.instances(where={"ecoe": ecoe})
    shifts = current_user.api_client.Shift.instances(where={"ecoe": ecoe})

    shifts_array = []
    for shift in shifts:
        planners = current_user.api_client.Planner.instances(where={"shift": shift})
        rounds_array = []
        for planner in planners:
            round = current_user.api_client.Round(planner.round.id)
            rounds_array.append(round.description)

        shifts_array.append({'shift': shift.time_start, 'rounds': rounds_array})

    return render_template('evaladmin.html', ecoe=ecoe, id_ecoe=id_ecoe, stations=station, planner=shifts_array )


# @bp.route('/evaluacion/<int: id>', methods=['GET'])
# def get_evaluacion(id):
#     return
