import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SERVER_NAME = "localhost:5080"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_ENABLED = False
    API_ROUTE = "http://10.1.56.79:5000/api"
