from flask import Blueprint

bp = Blueprint('ui_admin', __name__,
               template_folder='templates')

from app.ui_admin import routes, routes_question, routes_chronos
