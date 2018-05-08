from flask import render_template, flash, redirect, url_for
from app.ui_evaluation import bp
from potion_client import Client
from potion_client.auth import HTTPBearerAuth
from potion_client.exceptions import ItemNotFound
from config import Config

api_route = Config.API_ROUTE
client = Client(api_route)

@bp.route('/')
@bp.route('/index')
def index():
    ecoe = client.Ecoe.instances()
    return render_template('index.html', title='Home',  ecoes=ecoe)


@bp.route('/evaluacion', methods=['GET'])
@bp.route('/evaluacion/<int:i>', methods=['GET'])
def evaluacion():
    return render_template('evaluacion.html')

@bp.route('/evaladmin/', methods=['GET'])
@bp.route('/evaladmin/<int:id_ecoe>', methods=['GET'])
def evaladmin(id_ecoe):
    ecoe = client.Ecoe(id_ecoe)
    station = client.Station.instances(where={"ecoe": ecoe})
    shifts = client.Shift.instances(where={"ecoe": ecoe})

    shifts_array = []
    for shift in shifts:
        planners = client.Planner.instances(where={"shift": shift})
        rounds_array = []
        for planner in planners:
            round = client.Round(planner.round.id)
            rounds_array.append(round.description)

        shifts_array.append({'shift': shift.time_start, 'rounds': rounds_array})

    return render_template('evaladmin.html', ecoe=ecoe, id_ecoe=id_ecoe, stations=station, planner=shifts_array )


# @bp.route('/evaluacion/<int: id>', methods=['GET'])
# def get_evaluacion(id):
#     return
