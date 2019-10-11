from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '870f57857b5d5a3cabf12bd56fc535d7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diy_api.db'

db = SQLAlchemy(app)

from api import routes
