from flask import render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from app.ui_evaluation import bp
from potion_client.exceptions import ItemNotFound
from flask import request
from datetime import datetime
import pytz
import sys, operator
from collections import defaultdict


@bp.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    ecoe = current_user.api_client.Ecoe.instances()
    return render_template('eval_index.html', title='Home', ecoes=ecoe)


@bp.route('/ecoe/<int:id_ecoe>/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/round/<int:id_round>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/round/<int:id_round>/station/<int:id_station>', methods=['GET'])
@login_required
def evaladmin(id_ecoe, id_round=None, id_station=None):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    stations = []
    rounds = []

    now = datetime.now(pytz.utc)

    if id_station != None:
        stations.append(current_user.api_client.Station(id_station))
    else:
        stations = current_user.api_client.Station.instances(where={"ecoe": ecoe}, sort={"order": False})

    if id_round != None:
        rounds.append(current_user.api_client.Round(id_round))
    else:
        rounds = current_user.api_client.Round.instances(where={"ecoe": ecoe})

    shifts = current_user.api_client.Shift.instances(where={"ecoe": ecoe})

    shifts = filter(lambda shift: len(shift.planners) > 0, shifts)

    return render_template('eval_admin.html', ecoe=ecoe, stations=stations, rounds=rounds, now=now, shifts=shifts)


@bp.route(
    '/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>/order/<int:order_student>',
    methods=['GET'])
@login_required
def exam(id_ecoe, id_station, id_shift, id_round, order_student):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    actual_station = current_user.api_client.Station(id_station)
    planner = current_user.api_client.Planner.first(where={"shift": id_shift, "round": id_round})

    qblocks = current_user.api_client.Qblock.instances(where={"station": actual_station})

    stations_count = len(ecoe.stations)

    try:
        student = current_user.api_client.Student.first(where={"planner": planner, "planner_order": order_student})
    except ItemNotFound:
        student = None

    previous_student = order_student + 1
    next_student = order_student - 1

    if next_student <= 0:
        next_student = stations_count

    if previous_student > stations_count:
        previous_student = 1

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % planner.round.id

    return render_template('exam.html', chrono_route=chrono_route, ecoe=ecoe, station=actual_station, qblocks=qblocks,
                           planner=planner, student=student, order_student=order_student, next_student=next_student,
                           previous_student=previous_student)


@bp.route('/ecoe/<int:ecoe_id>/round/<int:round_id>/outside')
@login_required
def outside_station(ecoe_id, round_id):
    ecoe = current_user.api_client.Ecoe(ecoe_id)
    round = current_user.api_client.Round(round_id)

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % round_id

    return render_template('outside_station.html', chrono_route=chrono_route, ecoe=ecoe, round=round, station_id=0)


@bp.route('/student/<id_student>/option/<id_option>', methods=['POST','DELETE'])
@login_required
def send_answer(id_student, id_option):
    option = current_user.api_client.Option(id_option)
    student = current_user.api_client.Student(id_student)

    if request.method == 'POST':
        try:
            student.add_answers(option)
            return jsonify({'status': 204})
        except:
            print('Error al borrar', sys.exc_info()[0])
            return jsonify({'status': 404})

    elif request.method == 'DELETE':
        try:
            student.remove_answers(option)
            return jsonify({'status': 204})
        except:
            print('Error al borrar', sys.exc_info()[0])
            return jsonify({'status': 404})