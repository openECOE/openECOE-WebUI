from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddAreaForm(FlaskForm):
    name = StringField('Nueva Area', validators=[DataRequired()])
    submit = SubmitField('Añadir')

class EditAreaForm(FlaskForm):
    name = StringField('Nuevo nombre', validators=[DataRequired()])
    submit = SubmitField('Aceptar')

# class AddChronometerForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')

class AddStudentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    dni = PasswordField('DNI', validators=[DataRequired()])
    submit = SubmitField('Añadir')