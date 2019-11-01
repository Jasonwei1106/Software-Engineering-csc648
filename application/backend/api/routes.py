from flask import request, jsonify, make_response
from api import app, db, mysql
import yaml
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

            sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
            cur = mysql.connection.cursor()
            cur.execute(sql_query, (data['email_address'],))
            current_user = cur.fetchone()
            cur.close()

        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

## TO GET RID OF IN DEPLOYMENT ##
#################
### HOME PAGE ###
#################

@app.route('/api')
@app.route('/api/home')
def home():
    return jsonify({'message': 'Hello World!'})

######################
### USER FUNCTIONS ###
######################

@app.route('/api/user/get', methods=['GET'])
@token_required
def get_all_users(current_user):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM team206.users"
    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    users = cur.fetchall()
    cur.close()

    output = []

    for user in users:
        user_data = {}
        user_data['email_address'] = user[0]
        user_data['username'] = user[1]
        user_data['password'] = user[2]
        user_data['is_admin'] = user[3]
        user_data['avatar'] = user[4]
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/api/user/<email_address>', methods=['GET'])
@token_required
def get_one_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['email_address'] = user[0]
    user_data['username'] = user[1]
    user_data['password'] = user[2]
    user_data['is_admin'] = user[3]
    user_data['avatar'] = user[4]

    return jsonify({'users' : user_data})

@app.route('/api/user/current_user', methods=['GET'])
@token_required
def get_current_user(current_user):

    sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (current_user[0],))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['email_address'] = current_user[0]
    user_data['username'] = current_user[1]
    user_data['is_admin'] = current_user[3]
    user_data['password'] = '****'
    user_data['avatar'] = current_user[4]

    return jsonify({'current user' : user_data})

@app.route('/api/user/create', methods=['POST'])
def create_user():

    data = request.get_json()

    email_address = data['email_address']
    username = data['username']
    password = data['password']
    is_admin = '0'
    avatar = 'default.jpg'

    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO team206.users(email_address, username, password, is_admin, avatar) VALUES(%s, %s, %s, %s, %s)", (email_address, username, hashed_password, is_admin, avatar))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New user created!'})

@app.route('/api/user/<email_address>/promote', methods=['PUT'])
@token_required
def promote_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_update = "UPDATE team206.users SET is_admin = 1 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been promoted!'})

@app.route('/api/user/<email_address>/demote', methods=['PUT'])
@token_required
def demote_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_update = "UPDATE team206.users SET is_admin = 0 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been demoted!'})

@app.route('/api/user/<email_address>', methods=['DELETE'])
@token_required
def delete_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_delete = "DELETE FROM team206.users WHERE email_address=%s"
    cur.execute(sql_delete, (email_address,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been deleted!'})

### OLD LOGIN ROUTE
# @app.route('/api/login')
# def login():
#     auth = request.authorization
#
#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify auth', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
#
#     sql_query = "SELECT * FROM team206.users WHERE email_address=%s"
#     cur = mysql.connection.cursor()
#     cur.execute(sql_query, (auth.username,))
#     user = cur.fetchone()
#     cur.close()
#
#     if not user:
#         return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
#
#     if check_password_hash(user[2], auth.password):
#         token = jwt.encode({'email_address' : user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
#         # token = jwt.encode({'email_address' : user[0], app.config['SECRET_KEY'])
#         return jsonify({'token' : token.decode('UTF-8')})
#
#     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/api/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username:
        return make_response('Could not verify auth', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    sql_query = "SELECT * FROM team206.users WHERE username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user[2], password):
        token = jwt.encode({'email_address' : user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        # token = jwt.encode({'email_address' : user[0], app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

##########################
### TUTORIAL FUNCTIONS ###
##########################
@app.route('/api/tutorial/get', methods=['GET'])
def get_all_tutorials():
    sql_query = "SELECT * FROM team206.tutorials"
    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    tutorials = cur.fetchall()

    output = []

    for tutorial in tutorials:
        sql_query = "SELECT * FROM team206.steps WHERE tutorial_id=%s"
        cur.execute(sql_query, (tutorial[0],))
        steps = cur.fetchall()

        output_steps = []

        tutorial_data = {}
        tutorial_data['title'] = tutorial[1]
        tutorial_data['category'] = tutorial[3]
        tutorial_data['author_difficulty'] = str(tutorial[5])
        tutorial_data['viewer_difficulty'] = str(tutorial[6])
        tutorial_data['rating'] = str(tutorial[7])
        tutorial_data['author_id'] = tutorial[8]

        output.append(tutorial_data)

    cur.close()

    response = jsonify({'tutorials' : output})
    return response

@app.route('/api/tutorial/get_all', methods=['GET'])
def get_all_tutorial_info():
    sql_query = "SELECT * FROM team206.tutorials"
    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    tutorials = cur.fetchall()

    output = []

    for tutorial in tutorials:
        sql_query = "SELECT * FROM team206.steps WHERE tutorial_id=%s"
        cur.execute(sql_query, (tutorial[0],))
        steps = cur.fetchall()

        output_steps = []

        tutorial_data = {}
        tutorial_data['id'] = tutorial[0]
        tutorial_data['title'] = tutorial[1]
        tutorial_data['image'] = tutorial[2]
        tutorial_data['category'] = tutorial[3]
        tutorial_data['description'] = tutorial[4]
        tutorial_data['author_difficulty'] = str(tutorial[5])
        tutorial_data['viewer_difficulty'] = str(tutorial[6])
        tutorial_data['rating'] = str(tutorial[7])
        tutorial_data['author_id'] = tutorial[8]

        for step in steps:
            step_data = {}
            step_data['index'] = step[1]
            step_data['content'] = step[2]
            step_data['image'] = step[3]
            output_steps.append(step_data)

        tutorial_data['steps'] = output_steps

        output.append(tutorial_data)

    cur.close()

    response = jsonify({'tutorials' : output})
    return response

@app.route('/api/tutorial/<username>', methods=['GET'])
def get_all_tutorials_by_user(username):
    sql_query = "SELECT * FROM team206.tutorials WHERE author_id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    tutorials = cur.fetchall()

    if not tutorials:
        return jsonify({'message' : 'No tutorial found!'})

    output = []

    for tutorial in tutorials:
        sql_query = "SELECT * FROM team206.steps WHERE tutorial_id=%s"
        cur.execute(sql_query, (tutorial[0],))
        steps = cur.fetchall()

        output_steps = []

        tutorial_data = {}
        tutorial_data['id'] = tutorial[0]
        tutorial_data['title'] = tutorial[1]
        tutorial_data['image'] = tutorial[2]
        tutorial_data['category'] = tutorial[3]
        tutorial_data['description'] = tutorial[4]
        tutorial_data['author_difficulty'] = str(tutorial[5])
        tutorial_data['viewer_difficulty'] = str(tutorial[6])
        tutorial_data['rating'] = str(tutorial[7])
        tutorial_data['author_id'] = tutorial[8]

        for step in steps:
            step_data = {}
            step_data['index'] = step[1]
            step_data['content'] = step[2]
            step_data['image'] = step[3]
            output_steps.append(step_data)

        tutorial_data['steps'] = output_steps

        output.append(tutorial_data)

    cur.close()

    return jsonify({'tutorials' : output})

@app.route('/api/tutorial/<username>/<tutorial_id>', methods=['GET'])
def get_one_tutorial(username, tutorial_id):

    sql_query = "SELECT * FROM team206.tutorials WHERE author_id=%s AND id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username, int(tutorial_id)))
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    sql_query = "SELECT * FROM team206.steps WHERE tutorial_id=%s"
    cur.execute(sql_query, (tutorial[0],))
    steps = cur.fetchall()

    output_steps = []

    tutorial_data = {}
    tutorial_data['id'] = tutorial[0]
    tutorial_data['title'] = tutorial[1]
    tutorial_data['image'] = tutorial[2]
    tutorial_data['category'] = tutorial[3]
    tutorial_data['description'] = tutorial[4]
    tutorial_data['author_difficulty'] = str(tutorial[5])
    tutorial_data['viewer_difficulty'] = str(tutorial[6])
    tutorial_data['rating'] = str(tutorial[7])
    tutorial_data['author_id'] = tutorial[8]

    for step in steps:
        step_data = {}
        step_data['index'] = step[1]
        step_data['content'] = step[2]
        step_data['image'] = step[3]
        output_steps.append(step_data)

    tutorial_data['steps'] = output_steps

    cur.close()

    return jsonify({'tutorial' : tutorial_data})

@app.route('/api/tutorial/create', methods=['POST'])
@token_required
def create_tutorial(current_user):
    data = request.get_json()

    duplicate = True

    # To create new_set of UUID as a set
    # with open('api/uuid_set.yaml', 'w') as uuid_file:
    #     new_set = set()
    #     yaml.dump(new_set, uuid_file)

    # Read the set of existing UUIDs
    with open('api/uuid_set.yaml') as uuid_set_file:
        uuid_set = yaml.load(uuid_set_file)
        # Loop until a unique UUID is generated
        while duplicate is True:
            new_uuid = str(uuid.uuid4())
            if new_uuid not in uuid_set:
                duplicate = False

    with open('api/uuid_set.yaml', 'w') as uuid_set_file:
        # Add the new UUID to the set and dump it to the file
        uuid_set.add(new_uuid)
        yaml.dump(uuid_set, uuid_set_file)

    tutorial_uuid = new_uuid
    title = data['title']
    image = data['image']
    category = data['category']
    description = data['description']
    author_difficulty = data['author_difficulty']
    author_id = current_user[1]

    cur = mysql.connection.cursor()

    # For new db schema
    # cur.execute("INSERT INTO team206.tutorials(uuid, title, image, category, description, author_difficulty, author_id) VALUES(%s, %s, %s, %s, %s, %s, %s)", (tutorial_uuid, title, image, category, description, float(author_difficulty), author_id))

    cur.execute("INSERT INTO team206.tutorials(title, image, category, description, author_difficulty, author_id) VALUES(%s, %s, %s, %s, %s, %s)", (title, image, category, description, float(author_difficulty), author_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New tutorial created!'}, {'token' : tutorial_uuid})

## TEST TUTORIAL create
@app.route('/api/hidden/tutorial/<username>/create', methods=['POST'])
def create_tutorial_user(username):
    data = request.get_json()

    title = data['title']
    image = data['image']
    category = data['category']
    description = data['description']
    author_difficulty = data['author_difficulty']
    author_id = username

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM team206.users WHERE username=%s", (author_id,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user with that username exists.'})

    cur.execute("INSERT INTO team206.tutorials(title, image, category, description, author_difficulty, author_id) VALUES(%s, %s, %s, %s, %s, %s)", (title, image, category, description, float(author_difficulty), author_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New tutorial created!'})

@app.route('/api/tutorial/<username>/<tutorial_id>', methods=['DELETE'])
@token_required
def delete_tutorial(current_user, username, tutorial_id):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot delete tutorial of a different user!'}), 403

    sql_query = "SELECT * FROM team206.tutorials WHERE id=%s AND author_id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (int(tutorial_id), username,))
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    sql_delete = "DELETE FROM team206.tutorials WHERE id=%s AND author_id=%s"
    cur.execute(sql_delete, (int(tutorial_id), username,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Tutorial been deleted'})

######################
### STEP FUNCTIONS ###
######################

@app.route('/api/tutorial/<username>/<tutorial_id>/step', methods=['GET'])
def get_all_steps(tutorial_id, username):

    sql_query = "SELECT * FROM team206.steps INNER JOIN team206.tutorials ON steps.tutorial_id = tutorials.id WHERE tutorials.id=%s AND tutorials.author_id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (int(tutorial_id), username,))
    steps = cur.fetchall()
    cur.close()

    if not steps:
        return jsonify({'message' : 'No steps found for tutorial!'})

    output = []

    for step in steps:
        step_data = {}
        step_data['tutorial_id'] = step[0]
        step_data['index'] = step[1]
        step_data['content'] = step[2]
        step_data['image'] = step[3]
        output.append(step_data)

    return jsonify({'steps' : output})

@app.route('/api/tutorial/<username>/<tutorial_id>/step/<step_index>', methods=['GET'])
def get_one_step(username, tutorial_id, step_index):

    sql_query = "SELECT * FROM team206.steps INNER JOIN team206.tutorials ON steps.tutorial_id = tutorials.id WHERE tutorials.id=%s AND tutorials.author_id=%s AND steps.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (int(tutorial_id), username, step_index,))
    step = cur.fetchone()
    cur.close()

    if not step:
        return jsonify({'message' : 'No steps found for tutorial!'})

    step_data = {}
    step_data['tutorial_id'] = step[0]
    step_data['index'] = step[1]
    step_data['content'] = step[2]
    step_data['image'] = step[3]

    return jsonify({'steps' : step_data})

@app.route('/api/tutorial/<username>/<tutorial_id>/step/create', methods=['POST'])
@token_required
def create_tutorial_step(current_user, username, tutorial_id):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot create tutorial for a different user!'}), 403

    data = request.get_json()

    cur = mysql.connection.cursor()

    index = cur.execute("SELECT COUNT(*) FROM team206.steps WHERE team206.steps.tutorial_id=%s", (tutorial_id,))

    # May get rid of later
    if index != 0:
        index += 1

    content = data['content']
    image = data['image']

    cur.execute("INSERT INTO team206.steps(tutorial_id, steps.index, content, image) VALUES(%s, %s, %s, %s)", (tutorial_id, int(index), content, image,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been created'}, {'step id' : index})

@app.route('/api/tutorial/<username>/<tutorial_id>/step/<step_index>', methods=['DELETE'])
@token_required
def delete_tutorial_step(current_user, username, tutorial_id, step_index):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot delete tutorial step for a different user!'}), 403

    sql_query = "SELECT * FROM team206.steps INNER JOIN team206.tutorials ON steps.tutorial_id = tutorials.id WHERE tutorials.id=%s AND tutorials.author_id=%s AND steps.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (int(tutorial_id), username, step_index,))
    step = cur.fetchone()

    if not step:
        return jsonify({'message' : 'No step found for tutorial!'})

    sql_delete = "DELETE FROM team206.steps INNER JOIN team206.tutorials ON steps.tutorial_id = tutorials.id WHERE tutorials.id=%s AND tutorials.author_id=%s AND steps.index=%s"
    cur.execute(sql_query, (int(tutorial_id), username, step_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been deleted'})

########################
## COMMENTS FUNCTIONS ##
########################
@app.route('/api/tutorial/<username>/<tutorial_id>/comments/get_all', methods=['GET'])
def get_all_comments(username, tutorial_id):
    return ''

@app.route('/api/tutorial/<username>/<tutorial_id>/comments/get', methods=['GET'])
def get_comments(username, tutorial_id):
    return ''


######################
## RATING FUNCTIONs ##
######################
@app.route('/api/tutorial/<username>/<tutorial_id>/rate', methods=['POST'])
def user_rating(current_user, username, tutorial_id):
    return ''
