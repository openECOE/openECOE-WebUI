import os
from ast import literal_eval
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY =  os.environ.get('SECRET_KEY')
    DEBUG = literal_eval(os.environ.get('DEBUG'))
    TESTING = literal_eval(os.environ.get('TESTING'))
    API_ROUTE = os.environ.get('API_ROUTE')
    API_AUTH_TOKEN = os.environ.get('API_AUTH_TOKEN')
    CHRONO_ROUTE = os.environ.get('CHRONO_ROUTE')
    LANGUAGES = ['en', 'es']
    BOOTSTRAP_SERVE_LOCAL = True


