from flask import render_template, flash, redirect, url_for
from potion_client import Client
from ui_evaluation import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/evaluacion')
def evaluacion():
    return render_template('evaluacion.html')

@app.route('/evaluacion/<int: id>', methods=['GET'])
def get_evaluacion(id):
    return