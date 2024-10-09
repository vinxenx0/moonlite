# app/forms.py
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.user_model import Users

class NewUserRegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')


class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('usuario', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ConfigForm(FlaskForm):
    color_primary = StringField('Color primario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    color_secondary = StringField('Color secundario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    color_tertiary = StringField('Color terciario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    web_name = StringField('Nombre de la web', validators=[DataRequired()])
    logo_url = StringField('URL del logotipo', validators=[DataRequired(), URL()])

class PingForm(FlaskForm):
    domain = StringField('Dominio a pingear', validators=[DataRequired()])
    submit = SubmitField('Enviar')

    
class PageInfoForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Comprobar url')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar correo electrónico de recuperación')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Restablecer Contraseña')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Contraseña Antigua', validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[DataRequired()])
    submit = SubmitField('Cambiar Contraseña')


class EditProfileForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('usuario', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    active = BooleanField('Activo')
    submit = SubmitField('Guardar cambios')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')


class DomainToolsForm(FlaskForm):
    domain = StringField('Dominio', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SeoToolsForm(FlaskForm):
    domain = StringField('Página analizar incluyendo http o https', validators=[DataRequired()])
    submit = SubmitField('Enviar')