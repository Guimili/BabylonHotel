from datetime import datetime
from babylon import bcrypt
from babylon.models import Client, Room, Products
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, DateField, IntegerField, RadioField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Length

class BookingForm(FlaskForm):
    client = SelectField('Cliente', choices=[(c.name, c.name) for c in Client.query.all()] ,validators=[DataRequired(message='É necessário selecionar o Cliente!')])
    room = SelectField('Quarto', choices=[(str(r.number), r.number) for r in Room.query.filter_by(available=True).all()] ,validators=[DataRequired(message='É necessário selecionar o Quarto!')])
    # room = IntegerField('Quarto', validators=[DataRequired(message='É necessário fornecer o número do Quarto!')])
    check_in = DateTimeField('Entrada', validators=[DataRequired(message='É necessário fornecer a data de Check-in!')],\
        format="%Y-%m-%dT%H:%M")
    check_out = DateTimeField('Saída', validators=[DataRequired(message='É necessário fornecer a data do Check-out!')],\
        format="%Y-%m-%dT%H:%M")
    number = IntegerField('Numero de Pessoas', validators=[DataRequired(message='É necessário fornecer a quantidade de pessoas!'),\
        NumberRange(min=1, max=10, message='É permitido um máximo de 10 pessoas!')])
    submit = SubmitField('Fazer Reserva')

    def validate_check_in(self, check_in):
        if check_in.data < datetime.utcnow():
            raise ValidationError('A data de check-in deve ser posterior ao dia de hoje!')

    def validate_check_out(self, check_out):
        if check_out.data <= self.check_in.data:
            raise ValidationError('A data de check-out deve ser posterior à data de check-in!')

class ClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(message='É necessário fornecer o nome do Cliente!')])
    email = StringField('E-mail', validators=[DataRequired(message='É necessário fornecer um email!'),\
        Email('Email inserido é inválido!')])
    rg = StringField('RG' ,validators=[DataRequired('É necessário fornecer o RG!')])
    cpf = StringField('CPF', validators=[DataRequired('É necessário fornecer o CPF!')])
    birthdate = DateField('Data de Nascimento', validators=[DataRequired('É necessário inserir a data de nascimento!')],\
        format="%Y-%m-%d")
    phone = StringField('Telefone', validators=[DataRequired('É necessário fornecer um telefone para contato!'),\
        Length(min=10, max=11)])
    sex = RadioField(label='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])
    # cep = IntegerField(label="CEP", validators=[NumberRange(min=8, max=8)])
    address = StringField('Endereço', validators=[DataRequired('É necessário fornecer um endereço!')])
    submit = SubmitField()


    def validate_email(self, email):
        email = Client.query.filter_by(email=email.data).first()    
        if email:
           raise ValidationError('Email já utilizado!')

    def validate_rg(self, rg):
        rg = Client.query.filter_by(rg=rg.data).first()
        if rg:
            raise ValidationError('RG já utilizado!')

    def validate_cpf(self, cpf):
        cpf = Client.query.filter_by(cpf=cpf.data).first()    
        if cpf:
           raise ValidationError('CPF já utilizado!')

    def validate_phone(self, phone):
        phone = Client.query.filter_by(phone=phone.data).first()
        if phone:
            raise ValidationError('Telefone já utilizado!')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(message='É necessário fornecer um email!'),\
        Email('Email inserido é inválido!')])
    phone = StringField('Telefone', validators=[DataRequired('É necessário fornecer um telefone para contato!'),\
        Length(min=10, max=11)])
    sex = RadioField(label='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])
    address = StringField('Endereço', validators=[DataRequired('É necessário fornecer um endereço!')])
    submit = SubmitField()

    def validate_email(self, email):
        result = Client.query.filter_by(email=email.data).first()    
        if result and result.email != email.data:
           raise ValidationError('Email já utilizado!')

    def validate_phone(self, phone):
        result = Client.query.filter_by(phone=phone.data).first()
        if result and result.phone != phone.data:
            raise ValidationError('Telefone já utilizado!')

class SearchForm(FlaskForm):
    name = StringField('Nome')
    email = StringField('E-mail')
    rg = StringField('RG')
    cpf = StringField('CPF')
    phone = StringField('Telefone')
    submit = SubmitField('Buscar')

class ProductsForm(FlaskForm):
    products = SelectField('Produtos', choices=[(str(p.id), p.name) for p in Products.query.all()] ,validators=[DataRequired(message='É necessário selecionar um produto!')])
    submit = SubmitField('Adicionar')

