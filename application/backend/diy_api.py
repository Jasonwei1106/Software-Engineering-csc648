from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = '870f57857b5d5a3cabf12bd56fc535d7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diy_api.db'

db = SQLAlchemy(app)

class User(db.Model):
    email_address = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean)

class Tutorials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    user = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(120), nullable=False)

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    tutorial = db.Column(db.Integer)
    next = db.Column(db.Integer)
    previous = db.Column(db.Integer)

## Functions to make
# get_all
# get_one
# create_
# delete_

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(email_address=data['email_address']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.is_admin:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['email_address'] = user.email_address
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<email_address>', methods=['GET'])
@token_required
def get_one_user(current_user, email_address):

    if not current_user.is_admin:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['email_address'] = user.email_address
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['is_admin'] = user.is_admin

    return jsonify({'users' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.is_admin:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(email_address=data['email_address'], username=data['username'], password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<email_address>', methods=['PUT'])
@token_required
def promote_user(current_user, email_address):

    if not current_user.is_admin:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.is_admin = True
    db.session.commit()

    return jsonify({'message' : 'User has been promoted!'})

@app.route('/user/<email_address>', methods=['DELETE'])
@token_required
def delete_user(current_user, email_address):

    if not current_user.is_admin:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'User has been deleted'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email_address=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'email_address' : user.email_address, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

if __name__ == '__main__':
    app.run(debug=True)
