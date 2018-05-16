from flask import Blueprint

bp = Blueprint('ui_evaluation', __name__,
               template_folder='templates')

from app.ui_evaluation import routes
