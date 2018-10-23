from datetime import date, datetime
from flask import render_template, url_for, flash, redirect, request
from babylon import app
from babylon import db, bcrypt
from babylon.forms import BookingForm, LoginForm
from babylon.models import User, Employee
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
def home():
	return render_template('home.html', bookings = bookings, title = 'Home')

@login_required
@app.route('/register_booking', methods=['GET', 'POST'])
def register_booking():
	form = BookingForm()
	if form.validate_on_submit():
		flash('Reserva feita com sucesso!')
	return render_template('register_booking.html', title='Create Booking', form=form, timenow = date.today())


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

