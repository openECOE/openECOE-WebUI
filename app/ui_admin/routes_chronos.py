# -*- coding: utf-8 -*-
from flask import render_template, current_app, flash
from flask_login import login_required, current_user
from app.ui_admin import bp
import requests


def _load_chronos(ecoe):

    try:
        response = requests.post(current_app.config.get('CHRONO_ROUTE') + '/load',
                                 headers={'content-type': 'application/json'},
                                 json=ecoe.read_configuration())

        if response.status_code != 200:
            raise Exception(response.text)
    except Exception as e:
        return False, str(e)

    return True, 'OK'


@bp.route('/ecoe/<int:id_ecoe>/rounds')
@login_required
def roundsChronos(id_ecoe):
    ecoe = current_user.api_client.Ecoe.fetch(id_ecoe)

    return render_template('rounds_chronos.html', id_ecoe=id_ecoe, rounds=ecoe.rounds(), configuration=ecoe.read_configuration(), chrono_route=current_app.config.get('CHRONO_ROUTE'))


@bp.route('/ecoe/<int:id_ecoe>/start', methods=['POST'])
@login_required
def start_chronos(id_ecoe):

    ecoe = current_user.api_client.Ecoe(id_ecoe)

    try:
        loaded, message = _load_chronos(ecoe)

        if not loaded:
            raise Exception(message)

        # TODO: pass id_ecoe to URL
        response = requests.get(current_app.config.get('CHRONO_ROUTE') + '/start')

        if response.status_code != 200:
            raise Exception(response.text)
    except Exception as e:
        return str(e), 409

    return 'OK', 200


@bp.route('/ecoe/<int:id_ecoe>/<string:action>', methods=['POST'])
@bp.route('/ecoe/<int:id_ecoe>/<string:action>/<int:round_id>', methods=['POST'])
@login_required
def manage_chronos(id_ecoe, action, round_id=None):

    try:
        # TODO: pass id_ecoe to URL
        url = current_app.config.get('CHRONO_ROUTE') + '/' + action

        if round_id is not None:
            url = url + '/' + str(round_id)

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.text)
    except Exception as e:
        return str(e), 409

    return 'OK', 200

