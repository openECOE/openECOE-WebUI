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


@bp.route('/evaluacion')
def evaluacion():
    return render_template('evaluacion.html')

@bp.route('/evaladmin/', methods=['GET'])
@bp.route('/evaladmin/<int:id_ecoe>', methods=['GET'])
def evaladmin(id_ecoe):


    ecoe = client.Ecoe(id_ecoe)
    station = client.Station.instances(where={"ecoe": ecoe})
    days = client.Day.instances(where={"ecoe": ecoe})

    days_array=[]
    for day in days:
        shifts_array = []
        shifts = client.Shift.instances(where={"day": day})
        for shift in shifts:
            rounds_array = []
            rounds = client.Round.instances(where={"shift": shift})
            for round in rounds:
                rounds_array.append({"round": round.description})

            shifts_array.append({"shift": shift.start_time, "rounds": rounds_array})

        days_array.append({'day': day.date, "shifts": shifts_array})

    return render_template('evaladmin.html', ecoe=ecoe, id_ecoe=id_ecoe, stations=station, days=days_array )


# @bp.route('/evaluacion/<int: id>', methods=['GET'])
# def get_evaluacion(id):
#     return
