from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NoneOf, EqualTo

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=15), NoneOf({"secret","password"})])
    password2 = PasswordField('Repita su Contraseña', validators=[DataRequired(), EqualTo('password', 'Las contraseñas son distintas')])
    submit = SubmitField('Registro')


