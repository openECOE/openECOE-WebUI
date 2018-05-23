from flask import render_template, flash, redirect, url_for, current_app, make_response, jsonify, json
from flask_login import login_required, current_user
from app.ui_admin import bp
from app.ui_admin.forms import UploadCSVForm
from flask import request
import csv
from io import StringIO


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