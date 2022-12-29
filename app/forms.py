from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class TodoForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Crear')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')


class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')