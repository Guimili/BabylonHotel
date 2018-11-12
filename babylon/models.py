from datetime import datetime
from babylon import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60),nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('employee.id'), unique=True, nullable=False)

	def __repr__(self):
		return f"Usuario('{self.id}, {self.username}')"


class Employee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	cpf = db.Column(db.String(11), unique=True, nullable=False)
	role = db.Column(db.String(20), nullable=False)
	rg = db.Column(db.String(14), unique=True, nullable=False)
	birthdate = db.Column(db.Date, nullable=False)
	phone = db.Column(db.String(11), nullable=False)
	sex = db.Column(db.String(20), nullable=False)
	address = db.Column(db.String(120), nullable=False) 
	username = db.relationship('User', backref='employee', lazy=True)
	booking = db.relationship('Booking', backref='employee', lazy=True)

	def __repr__(self):
		return f"Funcionario('{self.id}', '{self.name}', '{self.cpf}','{self.email}')"

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	cpf = db.Column(db.String(11), unique=True, nullable=False)
	rg = db.Column(db.String(14), unique=True, nullable=False)
	birthdate = db.Column(db.Date, nullable=False)
	phone = db.Column(db.String(11), unique=True, nullable=False)
	sex = db.Column(db.String(20), nullable=False, default='Não declarado')
	address = db.Column(db.String(120), nullable=False) 
	booking = db.relationship('Booking', backref='client', lazy=True) 

	def __repr__(self):
		return f"Cliente('{self.id}', '{self.name}', '{self.cpf}')"

class Room(db.Model):
	number = db.Column(db.Integer, unique=True, primary_key=True)
	price = db.Column(db.Float, nullable=False)
	floor = db.Column(db.Integer, nullable=False)
	available = db.Column(db.Boolean, nullable=False, default=True)
	style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
	pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.id'), nullable=False)
	booking = db.relationship('Booking', backref='room', lazy=True)
	
	def __repr__(self):
		if self.available:
			return f"Quarto('{self.number}', '{self.available}', '{self.style}', '{self.pattern}')"

class Style(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	description = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Float, nullable=False)
	room = db.relationship('Room', backref='style', lazy=True)

	def __repr__(self):
		return f"Tipo: {self.name}\nDescrição: {self.description}"

class Pattern(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	description = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Float, unique=True, nullable=False)
	room = db.relationship('Room', backref='pattern', lazy=True)

	def __repr__(self):
		return f"Padrão: {self.name}\nDescrição: {self.description}"

class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	price = db.Column(db.Float, unique=True, nullable=False)
	booking = db.relationship('Booking_Products', backref='product', lazy=True)

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_booking = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_entry = db.Column(db.DateTime, nullable=False, default=datetime)
	date_exit = db.Column(db.DateTime, nullable=False, default=datetime)
	number_people = db.Column(db.Integer, nullable=False, default=1)
	price = db.Column(db.Float, nullable=False)
	concluded = db.Column(db.Boolean, nullable=False, default=False)
	room_number = db.Column(db.Integer, db.ForeignKey('room.number'), unique=True, nullable=False)
	employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

	def __repr__(self):
		return f"Reserva(ID: {self.id}, Quarto: {self.room_number}, Funcionario: {self}, Cliente: {self.client.name})"

class Booking_Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)