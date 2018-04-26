from flask import render_template, flash, redirect, url_for
from app.ui_admin import bp
from app.ui_admin.forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)
        )
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)
