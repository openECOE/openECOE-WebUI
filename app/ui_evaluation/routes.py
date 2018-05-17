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


@bp.route('/ecoe/', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/', methods=['GET'])
@login_required
def evaladmin(id_ecoe):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    station = current_user.api_client.Station.instances(where={"ecoe": ecoe})
    shifts = current_user.api_client.Shift.instances(where={"ecoe": ecoe})

    shifts_array = []
    uniques_rounds = []
    for shift in shifts:
        planners = current_user.api_client.Planner.instances(where={"shift": shift})
        rounds_array = []
        for planner in planners:
            round = current_user.api_client.Round(planner.round.id)
            rounds_array.append(round)
            uniques_rounds.append(round.round_code)
        shifts_array.append({'shift': shift, 'rounds': rounds_array})

    uniques_rounds = list(sorted(set(uniques_rounds)))
    return render_template('evaladmin.html', ecoe=ecoe, id_ecoe=id_ecoe, stations=station, planner=shifts_array, uniques_rounds=uniques_rounds)


@bp.route('/ecoe', methods=['GET'])
@bp.route('/ecoe/<int:id_ecoe>/station/<int:id_station>/shift/<int:id_shift>/round/<int:id_round>/student/<int:id_student>', methods=['GET'])
@login_required
def evaluacion(id_ecoe, id_station, id_shift, id_round, id_student):
    ecoe = current_user.api_client.Ecoe(id_ecoe)
    actual_station = current_user.api_client.Station(id_station)
    stations_count = len(current_user.api_client.Station.instances())
    shift = current_user.api_client.Shift(id_shift)
    round = current_user.api_client.Round(id_round)
    planner = current_user.api_client.Planner.instances(where={"shift": shift, "round": round})
    students = []
    if planner[0].students:
        students = planner[0].students

    previous_student = None
    actual_student = None
    next_student = None

    try:
        if (id_student + 1) > stations_count:
            previous_student = students[0]
        else:
            previous_student = current_user.api_client.Student(id_student + 1)
    except:
        previous_student = None

    try:
        actual_student = current_user.api_client.Student(id_student)
    except:
        actual_student = None

    try:
        if (id_student - 1) < 1:
            next_student = students[len(students) - 1]
        else:
            next_student = current_user.api_client.Student(id_student - 1)
    except:
        next_student = None

    # if actual_student is not None:
    #     exists = any(x.id == actual_student.id for x in students)
    #     if exists:
    #         students = [students[id_student - 2], students[id_student - 1], students[id_student]]

    students = [previous_student, actual_student, next_student]

    qblocks = actual_station.qblocks()
    questions_array = []
    for qblock in qblocks:
        questions = qblock.questions()
        for question in questions:
            options = current_user.api_client.Option.instances(where={"question": question}, sort={"order": False})
            questions_array.append({'question': question, 'options': options})

    chrono_route = current_app.config.get('CHRONO_ROUTE') + "/round%d" % round.id

    return render_template('evaluacion.html', chrono_route=chrono_route, ecoe=ecoe, station=actual_station, id_shift=shift.id, id_round=round.id, qblock=qblocks, questions=questions_array, students=students)


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


