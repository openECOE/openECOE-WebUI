import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import config

login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app():
    app_settings = os.getenv(
        'APP_SETTINGS',
        'config.DevelopmentConfig'
    )

    app = Flask(__name__)
    app.config.from_object(config)

    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app.ui_admin import bp as ui_admin_bp
    app.register_blueprint(ui_admin_bp, url_prefix='/admin')

    from app.ui_evaluation import bp as ui_eval_bp
    app.register_blueprint(ui_eval_bp, url_prefix = '/eval')

    return app