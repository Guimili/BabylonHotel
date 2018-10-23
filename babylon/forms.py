from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError


class BookingForm(FlaskForm):
    client = StringField('Cliente', validators=[DataRequired(message='É necessário fornecer o nome do Cliente!')])
    room = IntegerField('Quarto', validators=[DataRequired(message='É necessário fornecer o número do Quarto!')])
    check_in = DateTimeField('Entrada', validators=[DataRequired(message='É necessário fornecer a data de Check-in!')],\
        format="%Y-%m-%dT%H:%M")
    check_out = DateTimeField('Saída', validators=[DataRequired(message='É necessário fornecer o nome do Check-out!')],\
        format="%Y-%m-%dT%H:%M")
    number = IntegerField('Numero de Pessoas', validators=[DataRequired(message='É necessário fornecer a quantidade de pessoas!'),\
        NumberRange(min=1, max=10, message='É permitido um máximo de 10 pessoas!')])
    submit = SubmitField('Register')

    def validate_check_in(self, field):
        if field.data < datetime.utcnow():
            raise ValidationError('A data de check-in deve ser posterior ao dia de hoje!')

    def validate_check_out(self, field):
        if field.data < self.check_in.data:
            raise ValidationError('A data de check-out deve ser posterior à data de check-in!')



class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')


