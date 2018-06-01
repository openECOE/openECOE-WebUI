import unittest
from app import create_app
from config import Config
from ui_evaluation.tests import ApiClient
import app.ui_evaluation.routes as uiroutes
import app.auth.routes as authroutes


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True
    API_AUTH = True


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client_class = ApiClient
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_api_user(self):
        response = self.client.post('/auth/login', data={'email': 'fernando', 'password': 'fernando'})
        self.assert200(response)

    def test_evaladmin(self):
        response = uiroutes.evaladmin(1, 1, 1)
        self.assert200(response)

        response = uiroutes.evaladmin(2343)
        self.assert404(response)

        response = uiroutes.evaladmin(1, 2343)
        self.assert404(response)

        response = uiroutes.evaladmin(1, 1, 2343)
        self.assert404(response)

    # def test_exam(self):




# from flask_potion.routes import Route, ItemRoute
# from flask_potion import Api, fields
# from flask_potion.contrib.memory.manager import MemoryManager
# from flask_potion.resource import ModelResource, Resource
# from tests import BaseTestCase
#
# from flask_login import login_required, current_user
# import app.ui_evaluation.errors
#
#
# from flask import current_app
# from flask.testing import FlaskClient as BaseFlaskClient
# from flask_wtf.csrf import generate_csrf
#
# class RequestShim(object):
#
#     def __init__(self, client):
#         self.client = client
#
#     def set_cookie(self, key, value='', *args, **kwargs):
#         server_name = current_app.config.API_ROUTE
#         return self.client.set_cookie(
#             server_name, key=key, value=value, *args, **kwargs
#         )
#
#     def delete_cookie(self, key, *args, **kwargs):
#         server_name = current_app.config.API_ROUTE
#         return self.client.delete_cookie(
#             server_name, key=key, *args, **kwargs
#         )
#
#
# class FlaskClient(BaseFlaskClient):
#     @property
#     def csrf_token(self):
#         request = RequestShim(self)
#         environ_overrides = {}
#         self.cookie_jar.inject_wsgi(environ_overrides)
#         with flask.current_app.test_request_context(
#                 "/login", environ_overrides=environ_overrides,
#             ):
#             csrf_token = generate_csrf()
#             flask.current_app.save_session(flask.session, request)
#             return csrf_token
#
#
#     def login(self, email, password):
#         return self.post("/login", data={
#             "email": email,
#             "password": password,
#             "csrf_token": self.csrf_token,
#         }, follow_redirects=True)
#
#     def logout(self):
#         return self.get("/logout", follow_redirects=True)
#
#
#
# app = Flask(__name__)
# app.test_client_class = FlaskClient
#
# client = app.test_client()
#
# response = client.login('fernando','fernando')
# self.assert200(response)
# response = client.login('usuarioflask@ejemplo.com', 'usuarioflask')
# self.assert401(response)
#
# client.post("http://dev.api.openecoe.umh.es:5000/api/ecoe/1", data={
#     "id_organizacion": "20001"
# })
#
# class ApiTestCase(BaseTestCase):
#
#     def test_login(self):
#
#
#     def test_evaladmin(self):
#         # test ecoe
#         response = current_user.api_client.Ecoe(id_ecoe)
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/ecoe/2015")
#         self.assert404(response)
#
#         # test station
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/station/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/station/2015")
#         self.assert404(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/station?where={"ecoe":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/station?where={"ecoe":1}')
#         self.assert404(response)
#
#         # test round
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/rounds?where={"ecoe":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/rounds?where={"ecoe":1}')
#         self.assert404(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/round/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/round/2015")
#         self.assert404(response)
#
#         #test shift
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/shift?where={"ecoe":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/shift?where={"ecoe":1}')
#         self.assert404(response)
#
#     def test_eval(self):
#         #test ecoe
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/ecoe/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/ecoe/2015")
#         self.assert404(response)
#
#         #test station
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/station/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/station/2015")
#         self.assert404(response)
#
#         #test planner; falta saber como es en schema y como implementarlo aqui con las 5 funcionalidades
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/planner?where={"shift":1,"round":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/shift?where={"ecoe":1}')
#         self.assert404(response)
#
#         #test qblocks
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/qblocks?where={"ecoe":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/qblocks?where={"ecoe":1}')
#         self.assert404(response)
#
#         # test students; falta saber como es en schema y como implementarlo aqui con las 5 funcionalidades
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/students?where={"ecoe":1}')
#         self.assert200(response)
#         response = self.client.get('http://dev.api.openecoe.umh.es:5000/api/ecoe/1/students?where={"ecoe":1}')
#         self.assert404(response)
#
#         #test chrono
#
#     def test_outside_station(self):
#         # test answer
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/ecoe/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/ecoe/2015")
#         self.assert404(response)
#
#         # test round
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/round/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/round/2015")
#         self.assert404(response)
#
#         # test chrono
#
#     def test_send_answer(self):
#         # test answer
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/option/1")
#         self.assert200(response)
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/option/2015")
#         self.assert404(response)
#
#         # test student
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/student/1")
#         self.assert200(response)
#
#         if self.assert200(response):
#             response = self.client.post("http://dev.api.openecoe.umh.es:5000/api/student/1/answers", data=1)
#             self.assert200(response)
#             response = self.client.post("http://dev.api.openecoe.umh.es:5000/api/student/1/answers", data=50000)
#             self.assert404(response)
#
#
#         response = self.client.get("http://dev.api.openecoe.umh.es:5000/api/student/2015")
#         self.assert404(response)
#
#     def test_delete_answer(self):
#         #test answer
#         response = self.client.delete("http://dev.api.openecoe.umh.es:5000/api/option/1")
#         self.assert204(response)
#         response = self.client.delete("http://dev.api.openecoe.umh.es:5000/api/option/2015")
#         self.assert404(response)
#
#         #test student
#         response = self.client.delete("http://dev.api.openecoe.umh.es:5000/api/student/1")
#         self.assert204(response)
#         response = self.client.delete("http://dev.api.openecoe.umh.es:5000/api/student/2015")
#         self.assert404(response)