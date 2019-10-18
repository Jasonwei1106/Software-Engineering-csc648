from flask import request, jsonify, make_response
from api import app, db
from api.models import User, Tutorial, Step, Comment, List
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# Token used to authenticate user
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

## TO GET RID OF IN DEPLOYMENT ##
#################
### HOME PAGE ###
#################

@app.route('/')
@app.route('/home')
def home():
    return jsonify({'message': 'Hello World!'})

######################
### USER FUNCTIONS ###
######################

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

@app.route('/user/current_user', methods=['GET'])
@token_required
def get_current_user(current_user):

    user = User.query.filter_by(email_address=current_user.email_address).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['email_address'] = current_user.email_address
    user_data['username'] = current_user.username
    user_data['is_admin'] = current_user.is_admin

    return jsonify({'current user' : user_data})

@app.route('/user', methods=['POST'])
def create_user():

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
        token = jwt.encode({'email_address' : user.email_address, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

##########################
### TUTORIAL FUNCTIONS ###
##########################

@app.route('/tutorial', methods=['GET'])
@token_required
def get_all_tutorials(current_user):
    tutorials = Tutorial.query.all()

    output = []

    for tutorial in tutorials:
        steps = Step.query.filter_by(tutorial=tutorial.id).all()
        output_steps = []

        tutorial_data = {}
        tutorial_data['id'] = tutorial.id
        tutorial_data['title'] = tutorial.title
        tutorial_data['image'] = tutorial.image
        tutorial_data['description'] = tutorial.description
        tutorial_data['author_difficulty'] = tutorial.author_difficulty
        tutorial_data['viewer_difficulty'] = tutorial.viewer_difficulty
        tutorial_data['rating'] = tutorial.rating
        tutorial_data['username'] = tutorial.username

        for step in steps:
            step_data = {}
            step_data['index'] = step.index
            step_data['content'] = step.content
            step_data['image'] = step.image
            output_steps.append(step_data)

        tutorial_data['steps'] = output_steps

        output.append(tutorial_data)

    return jsonify({'tutorials' : output})

@app.route('/tutorial/<username>', methods=['GET'])
def get_all_tutorials_by_user(username):
    tutorials = Tutorial.query.filter_by(username=username).all()

    if not tutorials:
        return jsonify({'message' : 'No tutorial found!'})

    output = []

    for tutorial in tutorials:
        steps = Step.query.filter_by(tutorial=tutorial.id).all()
        output_steps = []

        tutorial_data = {}
        tutorial_data['id'] = tutorial.id
        tutorial_data['title'] = tutorial.title
        tutorial_data['image'] = tutorial.image
        tutorial_data['description'] = tutorial.description
        tutorial_data['author_difficulty'] = tutorial.author_difficulty
        tutorial_data['viewer_difficulty'] = tutorial.viewer_difficulty
        tutorial_data['rating'] = tutorial.rating
        tutorial_data['username'] = tutorial.username

        for step in steps:
            step_data = {}
            step_data['index'] = step.index
            step_data['content'] = step.content
            step_data['image'] = step.image
            output_steps.append(step_data)

        tutorial_data['steps'] = output_steps

        output.append(tutorial_data)

    return jsonify({'tutorials' : output})

@app.route('/tutorial/<username>/<tutorial_id>', methods=['GET'])
def get_one_tutorial(username, tutorial_id):

    tutorial = Tutorial.query.filter_by(username=username, id=tutorial_id).first()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    steps = Step.query.filter_by(tutorial=tutorial.id).all()
    output_steps = []

    tutorial_data = {}
    tutorial_data['id'] = tutorial.id
    tutorial_data['title'] = tutorial.title
    tutorial_data['image'] = tutorial.image
    tutorial_data['description'] = tutorial.description
    tutorial_data['author_difficulty'] = tutorial.author_difficulty
    tutorial_data['viewer_difficulty'] = tutorial.viewer_difficulty
    tutorial_data['rating'] = tutorial.rating
    tutorial_data['username'] = tutorial.username

    for step in steps:
        step_data = {}
        step_data['index'] = step.index
        step_data['content'] = step.content
        step_data['image'] = step.image
        output_steps.append(step_data)

    tutorial_data['steps'] = output_steps

    return jsonify({'tutorial' : tutorial_data})

@app.route('/tutorial', methods=['POST'])
@token_required
def create_tutorial(current_user):
    data = request.get_json()

    user = User.query.filter_by(username=current_user.username).first()

    new_tutorial = Tutorial(title=data['title'], image=data['image'], category=data['category'], description=data['description'], author_difficulty=data['author_difficulty'], tutorial_owner=user)

    db.session.add(new_tutorial)
    db.session.commit()

    return jsonify({'message' : 'New tutorial created!'})

@app.route('/tutorial/<username>/<tutorial_id>', methods=['DELETE'])
@token_required
def delete_tutorial(current_user, username, tutorial_id):
    if username != current_user.username or current_user.is_admin == False:
        return jsonify({'message' : 'Cannot delete tutorial of a different user!'}), 403

    tutorial = Tutorial.query.filter_by(id=tutorial_id, username=username).first()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    db.session.delete(tutorial)
    db.session.commit()

    return jsonify({'message' : 'Tutorial been deleted'})

######################
### STEP FUNCTIONS ###
######################

@app.route('/tutorial/<username>/<tutorial_id>/step', methods=['GET'])
def get_all_steps(username, tutorial_id):
    steps = Step.query.filter_by(tutorial=tutorial_id, user=username).all()

    if not steps:
        return jsonify({'message' : 'No steps found for tutorial!'})

    output = []

    for step in steps:
        step_data = {}
        step_data['index'] = step.index
        step_data['content'] = step.content
        step_data['image'] = step.image
        step_data['tutorial'] = step.tutorial
        step_data['user'] = step.user
        output.append(step_data)

    return jsonify({'steps' : output})

@app.route('/tutorial/<username>/<tutorial_id>/step/<step_index>', methods=['GET'])
def get_one_step(username, tutorial_id, step_index):
    steps = Step.query.filter_by(tutorial=tutorial_id, user=username, index=step_index).first()

    if not steps:
        return jsonify({'message' : 'No steps found for tutorial!'})

    step_data = {}
    step_data['index'] = step.index
    step_data['content'] = step.content
    step_data['image'] = step.image
    step_data['tutorial'] = step.tutorial
    step_data['user'] = step.user

    return jsonify({'steps' : step_data})

@app.route('/tutorial/<username>/<tutorial_id>/step', methods=['POST'])
@token_required
def create_tutorial_step(current_user, username, tutorial_id):
    if username != current_user.username or current_user.is_admin == False:
        return jsonify({'message' : 'Cannot create tutorial for a different user!'}), 403

    data = request.get_json()

    new_step = Step(content=data['content'], image=data['image'], tutorial=tutorial_id, user=username)

    db.session.add(new_step)
    db.session.commit()

    return jsonify({'message' : 'Step has been created'})

@app.route('/tutorial/<username>/<tutorial_id>/step/<step_index>', methods=['DELETE'])
@token_required
def delete_tutorial_step(current_user, username, tutorial_id, step_index):
    if username != current_user.username or current_user.is_admin == False:
        return jsonify({'message' : 'Cannot delete tutorial step for a different user!'}), 403

    step = Step.query.filter_by(user=username, tutorial=tutorial_id, index=step_index).first()

    if not step:
        return jsonify({'message' : 'No step found for tutorial!'})

    db.session.delete(step)
    db.session.commit()

    return jsonify({'message' : 'Step has been deleted'})

# Test list
@app.route('/test', methods=['GET'])
def test_route():
    return ''
