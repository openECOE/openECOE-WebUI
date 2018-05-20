from flask import render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from app.ui_evaluation import bp
from potion_client.exceptions import ItemNotFound
from flask import request
from datetime import datetime
import sys, operator

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
    return render_template('eval_index.html', title='Home',  ecoes=ecoe)


@bp.route('/ecoe/<int:id_ecoe>/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/round/<int:id_round>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/round/<int:id_round>/station/<int:id_station>', methods=['GET'])
@login_required
def evaladmin(id_ecoe, id_round=None, id_station=None):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    stations = []
    rounds = []

    if id_station != None:
        stations.append(current_user.api_client.Station(id_station))
    else:
        stations = current_user.api_client.Station.instances(where={"ecoe": ecoe}, sort={"order": False})

    if id_round != None:
        rounds.append(current_user.api_client.Round(id_round))
    else:
        rounds = current_user.api_client.Round.instances(where={"ecoe": ecoe})

    return render_template('eval_admin.html', ecoe=ecoe, stations=stations, rounds=rounds)


@bp.route('/ecoe', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>/order/<int:order_student>', methods=['GET'])
@login_required
def exam(id_ecoe, id_station, id_shift, id_round, order_student = None):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    actual_station = current_user.api_client.Station(id_station)
    planner = current_user.api_client.Planner.first(where={"shift": id_shift, "round": id_round})

    qblocks = current_user.api_client.Qblock.instances(where={"station": actual_station}, sort={"order": False})

    for qblock in qblocks:
        qblock.questions = sorted(qblock.questions, key=operator.attrgetter('order'))

    stations_count = len(ecoe.stations)

    if order_student is None:
        order_student = actual_station.order

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

    return render_template('exam.html', chrono_route=chrono_route, ecoe=ecoe, station=actual_station, qblocks=qblocks, planner=planner, student=student, order_student=order_student, next_student=next_student, previous_student=previous_student)


@bp.route('/ecoe/<int:ecoe_id>/round/<int:round_id>/outside')
@login_required
def outside_station(ecoe_id, round_id):
    ecoe = current_user.api_client.Ecoe(ecoe_id)
    round = current_user.api_client.Round(round_id)

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % round_id

    return render_template('outside_station.html', chrono_route=chrono_route, ecoe=ecoe, round=round, station_id=0)


@bp.route('/student/<id_student>/option/<id_option>/add', methods=['POST'])
@login_required
def send_answer(id_student, id_option):
    if request.method == 'POST':
        option = current_user.api_client.Option(id_option)
        student = current_user.api_client.Student(id_student)

        try:
            student.add_answers(option)
            return jsonify({'status': 204})
        except:
            flash('Error al borrar')
            print('Error')
            return jsonify({'status': 404})


@bp.route('/student/<id_student>/option/<id_option>/delete', methods=['DELETE'])
@login_required
def delete_answer(id_student, id_option):
    if request.method == 'DELETE':
        answer = current_user.api_client.Option(id_option)
        student = current_user.api_client.Student(id_student)

        try:
            student.remove_answers(answer)
            return jsonify({'status': 204})
        except:
            flash('Error al borrar')
            print('Error al borrar', sys.exc_info()[0])
            return jsonify({'status': 404})


