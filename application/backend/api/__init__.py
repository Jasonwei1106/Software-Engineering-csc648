from flask import Flask
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

app.config['SECRET_KEY'] = '870f57857b5d5a3cabf12bd56fc535d7'

db = yaml.load(open('api/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

from api import routes
