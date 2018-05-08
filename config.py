import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SERVER_NAME = "www.openecoe.com:5080"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_ENABLED = False
    API_HOST = "http://10.1.56.94:5000/api"
    API_ROUTE = "http://" + API_HOST + "/api"
    API_AUTH_TOKEN = "http://" + API_HOST + "/auth/tokens"
    LANGUAGES = ['en', 'es']
