# app/forms.py
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Optional, Regexp, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.user_model import Users
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class SubscriptionForm(FlaskForm):
    subscription_plan = SelectField('Plan de Suscripción', choices=[
        ('Free', 'Free - 0$'), 
        ('Pro', 'Pro - 9$'), 
        ('Corporate', 'Corporate - 129$')
    ], validators=[DataRequired()])
    subscription_currency = StringField('Moneda (ISO, e.g., USD, EUR)', validators=[DataRequired()])
    subscription_frequency = SelectField('Frecuencia de Pago', choices=[
        ('Monthly', 'Mensual'), 
        ('Annually', 'Anual')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Suscripción')


class PaymentForm(FlaskForm):
    primary_payment_method = SelectField('Método de Pago Primario', choices=[
        ('IBAN', 'IBAN'), ('SWIFT', 'SWIFT'), ('Bizum', 'Bizum'),
        ('PayPal', 'PayPal'), ('CreditCard', 'Tarjeta de Crédito')
    ], validators=[DataRequired()])
    primary_payment_details = StringField('Detalles del Método de Pago Primario', validators=[DataRequired()])
    
    secondary_payment_method = SelectField('Método de Pago Secundario', choices=[
        ('IBAN', 'IBAN'), ('SWIFT', 'SWIFT'), ('Bizum', 'Bizum'),
        ('PayPal', 'PayPal'), ('CreditCard', 'Tarjeta de Crédito')
    ])
    secondary_payment_details = StringField('Detalles del Método de Pago Secundario')

    submit = SubmitField('Guardar Métodos de Pago')


class NewUserRegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])

    # New subscription fields
    subscription_plan = SelectField('Plan de suscripción', choices=[('Free', 'Gratis'), ('Pro', 'Pro'), ('Corporate', 'Corporativo')], default='Free', validators=[DataRequired()])
    payment_frequency = SelectField('Frecuencia de pago', choices=[('Monthly', 'Mensual'), ('Annually', 'Anual')], validators=[DataRequired()], default='Monthly')

    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')

    def validate_payment_frequency(self, payment_frequency):
        # Ensure payment_frequency is only required if subscription is not 'Free'
        if self.subscription_plan.data == 'Free' and payment_frequency.data:
            raise ValidationError('La frecuencia de pago no es necesaria para el plan gratuito.')



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


class EditProfileForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password', message="Las contraseñas deben coincidir.")])
    role = SelectField('Rol', choices=[('admin', 'Admin'), ('usuario', 'Usuario')])
    active = BooleanField('Cuenta Activa')
    submit = SubmitField('Guardar Cambios')
