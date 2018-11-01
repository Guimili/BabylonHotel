from datetime import date, datetime
from hashlib import sha256
from flask import render_template, url_for, flash, redirect, request
from babylon import app, db, bcrypt
from babylon.forms import BookingForm, LoginForm, ClientForm, UpdateForm, SearchForm
from babylon.models import User, Client
from flask_login import login_user, current_user, logout_user, login_required

bookings = [
	{
		'employee': 'Liu',
		'room': 'Quarto 505',
		'booking_id': '1',
		'client': 'Vivi',
		'date_booking': '16/07/2018',
		'date_entrance': '20/10/2018',
		'date_exit': '30/10/2018',
	},
	{
		'employee': 'Liu',
		'room': 'Quarto 707',
		'booking_id': '2',
		'client': 'Laryza',
		'date_booking': '16/07/2018',
		'date_entrance': '25/10/2018',
		'date_exit': '35/10/2018',
	}
]

@app.route('/')
@login_required
def home():
	return render_template('home.html', bookings = bookings, title = 'Home')

@app.route('/register_booking', methods=['GET', 'POST'])
@login_required
def register_booking():
	form = BookingForm()
	if form.validate_on_submit():
		flash('Reserva feita com sucesso!')
	return render_template('register_booking.html', title='Criar Reserva', form=form)

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
		return redirect(url_for('home'))
	return render_template('register_client.html', title='Registrar Cliente', form=form)

@app.route('/search_client', methods=['GET', 'POST'])
@login_required
def search_client():
	form = SearchForm()
	if form.validate_on_submit():
		k, i = [], []
		for field in form:
			if field.name != 'submit' and field.name != 'csrf_token':
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

@app.route('/list_clients')
@login_required
def list_clients():
	page = request.args.get('page', 1, type=int)
	clients = Client.query.order_by(Client.name.asc()).paginate(per_page=4, page=page)
	return render_template('list_clients.html', title='Lista de Clientes', clients=clients)

@app.route('/client/<int:client_id>')
@login_required
def client(client_id):
	client = Client.query.get_or_404(client_id)
	return render_template('Client.html', title=client.name, client=client, today=date.today())
	
@app.route('/client/<int:client_id>/apagar', methods=['POST'])
@login_required
def delete_client(client_id):
	client = Client.query.get_or_404(client_id)
	db.session.delete(client)
	db.session.commit()
	flash('O Client foi descadastrado :(', 'success')
	return redirect(url_for('home'))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=False)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Falha ao logar. Confirme suas informações!', 'danger')
	return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

# @app.route('/conta')
# @login_required
# def account():
# 	return render_template('account.html', titulo = current_user.nome)

