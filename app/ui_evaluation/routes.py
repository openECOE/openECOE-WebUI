from flask import render_template, flash, redirect, url_for, current_app, jsonify, abort
from flask_login import login_required, current_user
from app.ui_evaluation import bp
from potion_client.exceptions import ItemNotFound
from flask import request
from datetime import datetime
import pytz
import sys, operator
from markupsafe import Markup
from collections import defaultdict


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


@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>/order/<int:order>',
          methods=['GET'])
@login_required
def exam(id_ecoe, id_station, id_shift, id_round, order=1):

    def get_stu_order(round_order, station, stations_cont):
        k = stations_cont - 1

        # Allow more rounds than stations to cycle students
        if round_order > stations_cont:
            round_order = round_order - stations_cont

        if round_order == 1:
            return station
        elif station == round_order - 1:
            return get_stu_order(round_order - 1, station, stations_cont) + k
        else:
            return get_stu_order(round_order - 1, station, stations_cont) - 1

    ecoe = current_user.api_client.Ecoe.fetch(id_ecoe)
    actual_station = current_user.api_client.Station(id_station)
    planner = current_user.api_client.Planner.first(where={"shift": id_shift, "round": id_round})

    qblocks = current_user.api_client.Qblock.instances(where={"station": actual_station})

    stations_count = len(ecoe.stations)

    order_student = get_stu_order(order, actual_station.order, stations_count)

    order_previous = order - 1
    order_next = order + 1

    if order_previous == 0:
        order_previous = None

    if (order_next > stations_count and actual_station.parent_station is None) \
            or order_next > stations_count + 1:  # Only allow one more round
        order_next = None

    try:
        student = current_user.api_client.Student.first(where={"planner": planner, "planner_order": order_student})

        for qblock in qblocks:
            for question in qblock.questions:
                options_set = set({option.id: option for option in question.options})
                answers_set = set({answer.id: answer for answer in student.answers})
                question.answers_ids = list(answers_set.intersection(options_set))
    except ItemNotFound:
        student = None

    #If it's an station with parent, first round doesn't apply for this student
    if actual_station.parent_station and order == 1:

        name_parent_station = str(actual_station.parent_station.order) + ' - ' + actual_station.parent_station.name
        student = None

        flash(Markup('<h3>Esta estación depende de la estación '
                     '<strong>'+name_parent_station+'</strong></h3>'
                    '<p>La primera vuelta no tiene asignado ningún alumno para su evaluación</p>'
                    '<p>El primer alumno se evalua en la última vuelta.</p>'),
              'warning')

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % planner.round.id

    return render_template('exam.html', chrono_route=chrono_route, ecoe=ecoe, station=actual_station, qblocks=qblocks,
                           planner=planner, student=student, order_next=order_next,
                           order_previous=order_previous)


@bp.route('/ecoe/<int:ecoe_id>/round/<int:round_id>/outside')
@login_required
def outside_station(ecoe_id, round_id):
    ecoe = current_user.api_client.Ecoe(ecoe_id)
    round = current_user.api_client.Round(round_id)

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % round_id

    return render_template('outside_station.html', chrono_route=chrono_route, ecoe=ecoe, round=round, station_id=0)


@bp.route('/student/<id_student>/option/<id_option>', methods=['POST', 'DELETE'])
@login_required
def send_answer(id_student, id_option):
    # TODO: Recover parameters by request form
    option = current_user.api_client.Option(id_option)
    student = current_user.api_client.Student(id_student)

    if request.method == 'POST':
        try:
            student.add_answers(option)
            return jsonify({'status': 204})
        except:
            print('POST answer error', sys.exc_info()[0])
            abort(404)

    elif request.method == 'DELETE':
        try:
            student.remove_answers(option)
            return jsonify({'status': 204})
        except:
            print('DELETE answer error', sys.exc_info()[0])
            abort(404)
