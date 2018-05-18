from flask import render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from app.ui_evaluation import bp
from potion_client.exceptions import ItemNotFound
from flask import request
import sys

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    ecoe = current_user.api_client.Ecoe.instances()
    return render_template('eval_index.html', title='Home',  ecoes=ecoe)


@bp.route('/ecoe/<int:id_ecoe>/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/round/<int:id_round>', methods=['GET'])
@login_required
def evaladmin(id_ecoe, id_station=None, id_round=None):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    station = []

    if id_station != None:
        station.append(current_user.api_client.Station(id_station))
    else:
        station = current_user.api_client.Station.instances(where={"ecoe": ecoe}, sort={"name": False})

    shifts = current_user.api_client.Shift.instances(where={"ecoe": ecoe})

    shifts_array = []
    uniques_rounds = []
    outside_rounds = {}

    for shift in shifts:
        planners_q = {"shift": shift}

        if id_round != None:
            planners_q.update({"round": id_round})

        planners = current_user.api_client.Planner.instances(where=planners_q)



        rounds_array = []
        for planner in planners:
            round = current_user.api_client.Round(planner.round.id)

            outside_rounds.update({round.round_code: round.id})

            rounds_array.append(round)
            uniques_rounds.append(round.round_code)
        shifts_array.append({'shift': shift, 'rounds': rounds_array})


    uniques_rounds = list(sorted(set(uniques_rounds)))
    return render_template('evaladmin.html', ecoe=ecoe, id_ecoe=id_ecoe, stations=station, planner=shifts_array, uniques_rounds=uniques_rounds, outside_rounds=outside_rounds)


@bp.route('/ecoe', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>/order/<int:order_student>', methods=['GET'])
@login_required
def exam(id_ecoe, id_station, id_shift, id_round, order_student):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    actual_station = current_user.api_client.Station(id_station)
    stations = current_user.api_client.Station.instances(where={"ecoe": id_ecoe}, sort={"name": False})
    stations_count = len(stations)
    planner = current_user.api_client.Planner.first(where={"shift": id_shift, "round": id_round})
    shift = planner.shift
    round = planner.round

    students = current_user.api_client.Student.instances(where={"planner": planner}, sort={"planner_order": False})

    previous_student = None
    actual_student = None
    next_student = None

    try:
        if (order_student + 1) > stations_count:
            previous_student = students[0]
        else:
            previous_student = students[order_student]
    except:
        previous_student = None

    try:
        actual_student = students[order_student - 1]
    except:
        actual_student = None

    try:
        if (order_student - 1) < 1:
            next_student = students[len(students) - 1]
        else:
            next_student = students[order_student - 2]
    except:
        next_student = None

    student_answers = []
    questions_array = []
    qblocks = []
    student_exists = False
    if actual_student is not None:
        student_exists = any(x.id == actual_student.id for x in students)
        if student_exists:
            student_answers = actual_student.answers

        qblocks = actual_station.qblocks()

        for qblock in qblocks:
            questions = qblock.questions()
            for question in questions:
                options = current_user.api_client.Option.instances(where={"question": question}, sort={"order": False})
                for answer in student_answers:
                    for opt in options:
                        if answer.id == opt.id:
                            opt.checked = True
                            break

                questions_array.append({'question': question, 'options': options})

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % round.id

    students_selector = [previous_student, actual_student, next_student]
    return render_template('exam.html', chrono_route=chrono_route, ecoe=ecoe, station=actual_station, shift=shift, round=round, qblock=qblocks, questions=questions_array, students=students_selector, student_exists=student_exists)


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


