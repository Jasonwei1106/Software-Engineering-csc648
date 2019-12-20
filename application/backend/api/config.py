from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_cors import CORS
import yaml

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = '870f57857b5d5a3cabf12bd56fc535d7'

# MySQL Configuration
db = yaml.load(open('api/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Flask-Mail Configuration
fm = yaml.load(open('api/fm.yaml'))
app.config['MAIL_SERVER'] = fm['mail_server']
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = fm['mail_username']
app.config['MAIL_PASSWORD'] = fm['mail_password']
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

from .routes import config
