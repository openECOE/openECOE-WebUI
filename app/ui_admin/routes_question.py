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
        question = current_user.api_client.Question.fetch(q_id)
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

        is_question = row['Opcion'] in (None, '')

        if is_question:

            # If qblock does not exist, must be created (general o specific)
            qblock_name = row.get('Bloque', 'General')

            try:
                qblock = current_user.api_client.Qblock.first(where={"station": station, "name": qblock_name})
            except ItemNotFound:
                qblock = current_user.api_client.Qblock()
                qblock.name = qblock_name
                qblock.order = 0
                qblock.station = station
                qblock.save()

            # Save questions
            question = current_user.api_client.Question()
            question.reference = row['Referencia'].strip()
            question.description = row['Enunciado'].strip()

            try:
                area = current_user.api_client.Area.first(where={"code": row['AC'], "ecoe": station.ecoe})

                question.area = area
            except HTTPError:
                raise Exception('Área desconocida para la pregunta %d' % int(row['Orden']))

            question.question_type = row['Tipo']
            question.order = int(row['Id'])
            question.save()

            # Many to many relationships
            qblock.add_questions(question)

        else:

            option = current_user.api_client.Option()
            option.points = float(row['Puntos'].replace(',', '.'))
            option.label = row['Referencia'].strip()
            option.order = int(row['Opcion'])
            option.question = question
            option.save()


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


