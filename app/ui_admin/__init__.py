from flask import Blueprint

bp = Blueprint('ui_admin', __name__,
               template_folder='templates')

from ui_admin import routes