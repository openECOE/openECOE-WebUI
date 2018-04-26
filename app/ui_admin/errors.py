from flask import render_template
from ui_admin import bp


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')


@bp.errorhandler(500)
def internal_error(error):
    return render_template('500.html')
