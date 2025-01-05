from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
#from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    primary_payment_method = SelectField('Método de Pago Primario',
                                         choices=[('IBAN', 'IBAN'),
                                                  ('SWIFT', 'SWIFT'),
                                                  ('Bizum', 'Bizum'),
                                                  ('PayPal', 'PayPal'),
                                                  ('CreditCard',
                                                   'Tarjeta de Crédito')],
                                         validators=[DataRequired()])
    primary_payment_details = StringField(
        'Detalles del Método de Pago Primario', validators=[DataRequired()])

    secondary_payment_method = SelectField('Método de Pago Secundario',
                                           choices=[('IBAN', 'IBAN'),
                                                    ('SWIFT', 'SWIFT'),
                                                    ('Bizum', 'Bizum'),
                                                    ('PayPal', 'PayPal'),
                                                    ('CreditCard',
                                                     'Tarjeta de Crédito')])
    secondary_payment_details = StringField(
        'Detalles del Método de Pago Secundario')

    submit = SubmitField('Guardar Métodos de Pago')
