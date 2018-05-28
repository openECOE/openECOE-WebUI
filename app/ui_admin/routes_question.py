# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from potion_client.exceptions import ItemNotFound
from requests.exceptions import HTTPError
from app.ui_admin import bp
from app.ui_admin.forms import UploadCSVForm
from flask import request
import csv
from io import StringIO


def _change_qblock(questions_id, station, qblock_target_name):

    try:
        qblock_target = current_user.api_client.Qblock.first(where={"name": qblock_target_name, "station": station})
    except:
        qblock_target = current_user.api_client.Qblock()
        qblock_target.name = qblock_target_name
        qblock_target.order = 0
        qblock_target.station = station
        qblock_target.save()

    for q_id in questions_id:
        question = current_user.api_client.Question(q_id)
        qblock_origin = current_user.api_client.Qblock(question.qblocks[0].id)

        if qblock_origin.id == qblock_target.id:
            raise Exception('No se puede cambiar al mismo bloque')

        qblock_target.add_questions(question)
        qblock_origin.remove_questions(question)


@bp.route('/station/<int:id_station>/questions', methods=['GET', 'POST'])
@login_required
def questions(id_station):

    station = current_user.api_client.Station(id_station)

    if request.method == 'GET':

        # TODO: create qblock_type in database model
        qblocks = current_user.api_client.Qblock.instances(where={"station": station}, sort={"order": False})
        qblock_types = [qb.name for qb in qblocks]

        if 'General' not in qblock_types:
            qblock_types.append('General')

        if 'Comunicación' not in qblock_types:
            qblock_types.append('Comunicación')

        uploadCSVform = UploadCSVForm(request.form)

        return render_template('station-questions.html',
                               station=station,
                               qblock_types=qblock_types,
                               qblocks=qblocks,
                               uploadCSVform=uploadCSVform)

    elif request.method == 'POST':

        post_action = request.form.get('post_action')

        if post_action == 'change_qblock':

            questions_id = request.form.getlist('question_id')
            qblock_target = request.form.get('qblock_target')

            try:
                _change_qblock(map(int, questions_id), station, qblock_target)
                flash('%d preguntas cambiadas al bloque %s' % (len(questions_id), qblock_target))
            except Exception as e:
                flash(str(e), category='error')

        return redirect(url_for('.questions', id_station=id_station))


def _load_csv(station):

    try:
        file = request.files['csv']

        if file.filename == '':
            raise Exception
    except:
        raise Exception('No se ha indicado el fichero')

    try:
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
    except:
        raise Exception('No se ha podido leer el fichero. Compruebe que el formato sea CSV')

    for row in csv_input:

        # 1. If there are not qblocks, one must be created
        try:
            qblock = current_user.api_client.Qblock.first(where={"station": station, "name": 'General'})
        except ItemNotFound:
            qblock = current_user.api_client.Qblock()
            qblock.name = 'General'
            qblock.order = 1
            qblock.station = station
            qblock.save()

        # 2. Save questions
        question = current_user.api_client.Question()
        question.reference = row['Referencia'].strip()
        question.description = row['Enunciado'].strip()

        try:
            area = current_user.api_client.Area(int(row['AC']))

            if area.ecoe != station.ecoe:
                raise Exception('El área %d no corresponde con la ECOE de la estación' % area.id)

            question.area = area
        except HTTPError:
            raise Exception('Área desconocida para la pregunta %d' % int(row['Orden']))

        question.question_type = 'CH'
        question.order = int(row['Orden'])
        question.save()

        # 3. Save options
        option_yes = current_user.api_client.Option()
        option_yes.points = int(row['Puntos'])
        option_yes.label = 'Sí'
        option_yes.order = 0
        option_yes.question = question
        option_yes.save()

        option_no = current_user.api_client.Option()
        option_no.points = 0
        option_no.label = 'No'
        option_no.order = 1
        option_no.question = question
        option_no.save()

        # 4. Many to many relationships
        qblock.add_questions(question)


@bp.route('/station/<int:id_station>/load_questions', methods=['POST'])
@login_required
def load_questions(id_station):

    station = current_user.api_client.Station(id_station)

    try:
        _load_csv(station)
    except Exception as e:
        flash(str(e), category='error')
    else:
        flash('Preguntas cargadas correctamente')

    return redirect(url_for('.questions', id_station=id_station))


