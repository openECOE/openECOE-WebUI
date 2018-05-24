# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, current_app, make_response, jsonify, json
from flask_login import login_required, current_user
from potion_client.exceptions import ItemNotFound
from app.ui_admin import bp
from app.ui_admin.forms import UploadCSVForm
from flask import request
import csv
from io import StringIO


def _load_questions(station):

    try:
        file = request.files['csv']

        if file.filename == '':
            raise Exception('No se ha indicado el fichero')
    except Exception as e:
        flash(e.message)
        return redirect(request.url)

    try:
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
    except:
        flash('No se ha podido leer el fichero. Compruebe que el formato sea CSV')
        return redirect(request.url)

    for row in csv_input:

        # 1. If there are not qblocks, one must be created
        try:
            qblock = current_user.api_client.Qblock.first(where={"station": station, "name": 'General'})
        except ItemNotFound:
            qblock = current_user.api_client.Qblock()
            qblock.name = 'General'
            qblock.order = 1
            qblock.station = station

        # 2. Save questions
        question = current_user.api_client.Question()
        question.reference = row['Referencia'].strip()
        question.description = row['Enunciado'].strip()

        #TODO: check area belongs to same ecoe
        try:
            area = current_user.api_client.Area(int(row['AC']))
            question.area = area
        except ItemNotFound:
            flash('Área desconocida')

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


@bp.route('/station/<int:id_station>/questions', methods=['GET', 'POST'])
@login_required
def questions(id_station):

    station = current_user.api_client.Station(id_station)

    if request.method == 'GET':

        uploadCSVform = UploadCSVForm(request.form)
        qblocks = current_user.api_client.Qblock.instances(where={"station": station}, sort={"order": False})

        #TODO: create qblock_type in database model
        qblock_types = [qb.name for qb in qblocks] if len(qblocks) > 0 else ['General', 'Comunicación']

        return render_template('station-questions.html', station=station, qblock_types=qblock_types, qblocks=qblocks, uploadCSVform=uploadCSVform)

    elif request.method == 'POST':

        _load_questions(station)
        flash('Preguntas cargadas correctamente')

        return redirect(url_for('.questions', id_station=id_station))


@bp.route('/ecoe/<int:id_ecoe>/load/questions', methods=['GET', 'POST'])
@login_required
def load_questions(id_ecoe):

    if request.method == 'GET':

        loadQuestionsForm = UploadCSVForm(request.form)
        return render_template('upload_csv.html', form=loadQuestionsForm)

    else:

        if 'csv' not in request.files:
            flash('No se ha indicado el fichero')
            return redirect(request.url)

        file = request.files['csv']

        if file.filename == '':
            flash('No se ha indicado el fichero')
            return redirect(request.url)

        try:
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.DictReader(stream)
        except:
            flash('No se ha podido leer el fichero. Compruebe que el formato sea CSV')
            return redirect(request.url)

        if file:
            return render_template('csvtable.html', data=csv_input)