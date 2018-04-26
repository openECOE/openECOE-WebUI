from flask import render_template
from ui_evaluation import app

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')