from flask import Flask, render_template, request
from config import Config

import json

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/validate', methods=['POST'])
def validate():
    return render_template("mainPage.html")


@app.route('/test/station/<int:id_station>')
def test(id_station):

    #Data
    open_file = open("datos.json", "r", encoding="utf-8")
    json_data = json.load(open_file)
    open_file.close()

    #with open("datos.json", "r", encoding="utf-8") as json_reader:

    ecoe_name = json_data["ECOE"]["Nombre"]
    estation_name = json_data["Estacion"]["Nombre"]
    user_name = json_data["Usuario"]["Nombre"]
    cod_day = json_data["Dia"]["cod_dia"]
    cod_turno = json_data["Turno"]["cod_turno"]
    cod_rueda = json_data["Rueda"]["cod_rueda"]

    #Questions
    open_questions = open("questions.json", "r", encoding="utf-8")
    json_questions = json.load(open_questions)
    open_questions.close()

    questions = json_questions["Preguntas"]

    #students
    open_students = open("studentTest.json", "r", encoding="utf-8")
    json_students = json.load(open_students)
    open_students.close()

    students = json_students["Alumnos"][0]



    return render_template("test.html", ecoe_name=ecoe_name, estation_name=estation_name, user_name=user_name, cod_day=cod_day, cod_turno=cod_turno, cod_rueda=cod_rueda, question=questions, students=students)

#@app.route('/nextStudent', methods=['POST'])
#def nextStudent():
