from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = '91e0cdbafbe43afeeff30b39ae342e24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from babylon import routes

