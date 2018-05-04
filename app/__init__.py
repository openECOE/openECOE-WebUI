import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app.ui_admin import bp as ui_admin_bp
    app.register_blueprint(ui_admin_bp, url_prefix='/admin')

    return app