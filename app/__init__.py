import os
from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from potion_client import Client
from flask_babel import Babel
from flask_wtf import CSRFProtect
from flask_moment import Moment
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
babel = Babel()
csrf = CSRFProtect()
moment = Moment()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

    from app.ui_admin import bp as ui_admin_bp
    app.register_blueprint(ui_admin_bp, url_prefix='/admin')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.ui_evaluation import bp as ui_eval_bp
    app.register_blueprint(ui_eval_bp, url_prefix = '/eval')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])