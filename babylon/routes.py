from datetime import date, datetime
from flask import render_template, url_for, flash, redirect, request
from babylon import app, db, bcrypt
from babylon.forms import BookingForm, LoginForm, ClientForm, UpdateForm, SearchForm, ProductsForm
from babylon.models import User, Client, Room, Booking, Products, Booking_Products, Employee
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/bookings')
@login_required
def bookings():
	page = request.args.get('page', 1, type=int)
	bookings = Booking.query.filter_by(concluded=False).order_by(Booking.date_exit.asc()).paginate(per_page=4, page=page)
	return render_template('bookings.html', bookings = bookings, title = 'bookings')

@app.route('/register_booking', methods=['GET', 'POST'])
@login_required
def register_booking():
	form = BookingForm()
	clients = Client.query.all()
	if form.validate_on_submit():
		price = (float(Room.query.filter_by(number=form.room.data).first().style.price)\
			+ float(Room.query.filter_by(number=form.room.data).first().pattern.price))\
			* (form.check_out.data - form.check_in.data).days
		booking = Booking(date_booking=date.today(),\
			date_entry=form.check_in.data,\
			date_exit=form.check_out.data,\
			number_people=form.number.data,\
			room_number=form.room.data,\
			price=price,\
			concluded=False,\
			employee_id=current_user.employee.id,\
			client_id=Client.query.filter_by(name=form.client.data).first().id)
		room = Room.query.filter_by(id=form.room.data).first()
		room.available = False
		db.session.add(booking)
		db.session.commit()
		flash('Reserva feita com sucesso!')
	return render_template('register_booking.html', title='Criar Reserva', form=form, clients=clients)

@app.route('/register_client', methods=['GET', 'POST'])
@login_required
def register_client():
	form = ClientForm()
	if form.validate_on_submit():
		client = Client(name=form.name.data,\
			email=form.email.data,\
			rg = form.rg.data,\
			cpf = form.cpf.data,\
			birthdate = form.birthdate.data,\
			phone = form.phone.data,\
			sex = form.sex.data,\
			address = form.address.data)
		db.session.add(client)
		db.session.commit()
		flash('Cliente registrado com sucesso!', 'success')
		return redirect(url_for('bookings'))
	return render_template('register_client.html', title='Registrar Cliente', form=form)

@app.route('/booking/<int:booking_id>')
@login_required
def booking(booking_id):
	booking = Booking.query.get_or_404(booking_id)
	products = Booking_Products.query.filter_by(booking_id=booking.id).all()
	return render_template('booking.html', title=f'Reserva #{booking.id}', booking=booking, products=products,\
		Booking=Booking)

	
@app.route('/booking/<int:booking_id>/apagar', methods=['POST'])
@login_required
def cancel_booking(booking_id):
	booking = Booking.query.get_or_404(booking_id)
	db.session.delete(booking)
	db.session.commit()
	flash('A reserva foi cancelada :(', 'success')
	return redirect(url_for('bookings'))

@app.route('/search_client', methods=['GET', 'POST'])
@login_required
def search_client():
	form = SearchForm()
	if form.validate_on_submit():
		k, i = [], []
		for field in form:
			if  field.name != 'csrf_token' and field.name != 'submit':
				if field.data:
					k.append(field.name)
					i.append(field.data)
		kwargs = dict(zip(k,i))
		if kwargs:
			client = Client.query.filter_by(**kwargs).first()
			if client:
				return redirect(url_for('client', client_id=client.id))
			else:
				flash('Não há cliente com as informações inseridas!')
				return redirect(url_for('search_client'))
		else:
			flash('Insira alguma informação!')
			return redirect(url_for('search_client'))


	return render_template('search_client.html', title='Buscar Cliente', form=form)

@app.route('/clients')
@login_required
def clients():
	page = request.args.get('page', 1, type=int)
	clients = Client.query.order_by(Client.name.asc()).paginate(per_page=4, page=page)
	return render_template('clients.html', title='Lista de Clientes', clients=clients)

@app.route('/employees')
@login_required
def employees():
	page = request.args.get('page', 1, type=int)
	employees = Employee.query.order_by(Employee.name.asc()).paginate(per_page=4, page=page)
	return render_template('employees.html', title='Lista de Funcionários', employees=employees)

@app.route('/concluded_bookings')
@login_required
def concluded_bookings():
	page = request.args.get('page', 1, type=int)
	bookings = Booking.query.filter_by(concluded=True).order_by(Booking.date_exit.asc()).paginate(per_page=4, page=page)
	return render_template('bookings.html', bookings = bookings, title = 'bookings')

@app.route('/client/<int:client_id>')
@login_required
def client(client_id):
	client = Client.query.get_or_404(client_id)
	booking = Booking.query.filter_by(client_id=client_id).first()
	return render_template('Client.html', title=client.name, client=client, booking=booking, today=date.today())

@app.route('/employee/<int:employee_id>')
@login_required
def employee(employee_id):
	page=request.args.get('page', 1, type=int)
	employee = Employee.query.get_or_404(employee_id).order_by(Employee.role.asc())
	bookings = Booking.query.filter_by(employee=employee, concluded=False).order_by(Booking.concluded.asc()).paginate(per_page=4, page=page)
	return render_template('employee.html', title=employee.name, employee=employee, today=date.today(), bookings=bookings)
	
@app.route('/client/<int:client_id>/apagar', methods=['POST'])
@login_required
def delete_client(client_id):
	client = Client.query.get_or_404(client_id)
	db.session.delete(client)
	db.session.commit()
	flash('O Client foi descadastrado :(', 'success')
	return redirect(url_for('bookings'))

@app.route('/client/<int:client_id>/update', methods=['GET', 'POST'])
@login_required
def update_client(client_id):
	client = Client.query.get_or_404(client_id)
	form = UpdateForm()
	if form.validate_on_submit():
		client.email=form.email.data
		client.phone = form.phone.data
		client.sex = form.sex.data
		client.address = form.address.data
		db.session.commit()
		flash('Os dados do cliente foram atualizados!', 'success')
		return redirect(url_for('client', client_id=client.id))
	elif request.method == 'GET' :	
		form.email.data = client.email
		form.phone.data = client.phone
		form.sex.data = client.sex
		form.address.data = client.address
	return render_template('update_client.html', title="Atualizar Cadastro", form=form, legend='Atualizar Cadastro')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('bookings'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=False)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('bookings'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('bookings'))

@app.route('/add_products/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def add_products(booking_id):
	form = ProductsForm()
	booking = Booking.query.get_or_404(booking_id)
	if form.validate_on_submit():
		products = Booking_Products(\
			booking_id=booking_id,\
			product_id=int(form.products.data))
		booking.price = booking.price + Products.query.get(int(form.products.data)).price 
		db.session.add(products)
		db.session.commit()
		flash('Adicionado!', 'success')
		return redirect(url_for('booking', booking_id=booking_id))
	return render_template('add_products.html', form=form)

@app.route('/conclude_booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def conclude_booking(booking_id):
	booking = Booking.query.get(booking_id)
	booking.concluded = True
	db.session.commit()
	flash('Reserva Finalizada =)')
	return redirect(url_for('bookings'))

@app.route('/list_available_rooms')
@login_required
def list_available_rooms():
	rooms = Room.query.filter_by(available=True).all()
	return render_template('rooms.html', rooms=rooms, title='Disponíveis')

@app.route('/list_unavailable_rooms')
@login_required
def list_unvailable_rooms():
	rooms = Room.query.filter_by(available=False).all()
	return render_template('rooms.html', rooms=rooms, title='Reservados')

# @app.route('/conta')
# @login_required
# def account():
# 	return render_template('account.html', titulo = current_user.nome)

