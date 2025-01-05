from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
#from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Correo electrónico',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar correo electrónico de recuperación')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Nueva Contraseña',
                             validators=[DataRequired(),
                                         Length(min=6)])
    confirm_password = PasswordField(
        'Confirmar Nueva Contraseña',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Restablecer Contraseña')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Contraseña Antigua',
                                 validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña',
                             validators=[DataRequired(),
                                         Length(min=6)])
    confirm_password = PasswordField('Confirmar Nueva Contraseña',
                                     validators=[DataRequired()])
    submit = SubmitField('Cambiar Contraseña')
