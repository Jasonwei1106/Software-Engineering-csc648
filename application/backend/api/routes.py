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

            sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
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

    sql_query = "SELECT * FROM diyup.users"
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

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
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

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
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
    cur.execute("INSERT INTO diyup.users(email_address, username, password, is_admin, avatar) VALUES(%s, %s, %s, %s, %s)", (email_address, username, hashed_password, is_admin, avatar))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New user created!'})

@app.route('/api/user/<email_address>/promote', methods=['PUT'])
@token_required
def promote_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_update = "UPDATE diyup.users SET is_admin = 1 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been promoted!'})

@app.route('/api/user/<email_address>/demote', methods=['PUT'])
@token_required
def demote_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_update = "UPDATE diyup.users SET is_admin = 0 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been demoted!'})

@app.route('/api/user/<email_address>', methods=['DELETE'])
@token_required
def delete_user(current_user, email_address):

    if current_user[3] != True:
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'})

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'})

    sql_delete = "DELETE FROM diyup.users WHERE email_address=%s"
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

    sql_query = "SELECT * FROM diyup.users WHERE username=%s"
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
    sql_query = "SELECT * FROM diyup.tutorials"
    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    tutorials = cur.fetchall()

    output = []

    for tutorial in tutorials:

        tutorial_data = {}
        tutorial_data['author_username'] = tutorial[1]
        tutorial_data['title'] = tutorial[2]
        tutorial_data['category'] = tutorial[4]
        tutorial_data['author_difficulty'] = str(tutorial[6])
        tutorial_data['viewer_difficulty'] = str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = str(average_rating_type_for_tutorial('score', tutorial[0]))

        output.append(tutorial_data)

    cur.close()

    response = jsonify({'tutorials' : output})
    return response

@app.route('/api/tutorial/get_all', methods=['GET'])
def get_all_tutorial_info():
    sql_query = "SELECT * FROM diyup.tutorials"
    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    tutorials = cur.fetchall()

    output = []

    for tutorial in tutorials:

        tutorial_data = {}
        tutorial_data['uuid'] = tutorial[0]
        tutorial_data['author_username'] = tutorial[1]
        tutorial_data['title'] = tutorial[2]
        tutorial_data['image'] = tutorial[3]
        tutorial_data['category'] = tutorial[4]
        tutorial_data['description'] = tutorial[5]
        tutorial_data['author_difficulty'] = str(tutorial[6])
        tutorial_data['viewer_difficulty'] = str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = str(average_rating_type_for_tutorial('score', tutorial[0]))
        
        sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s"
        cur.execute(sql_query, (tutorial[0],))
        steps = cur.fetchall()

        output_steps = []
        
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
    sql_query = "SELECT * FROM diyup.tutorials WHERE author_username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    tutorials = cur.fetchall()

    if not tutorials:
        return jsonify({'message' : 'No tutorial found!'})

    output = []

    for tutorial in tutorials:
        sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s"
        cur.execute(sql_query, (tutorial[0],))
        steps = cur.fetchall()

        output_steps = []

        tutorial_data = {}
        tutorial_data['uuid'] = tutorial[0]
        tutorial_data['author_username'] = tutorial[1]
        tutorial_data['title'] = tutorial[2]
        tutorial_data['image'] = tutorial[3]
        tutorial_data['category'] = tutorial[4]
        tutorial_data['description'] = tutorial[5]
        tutorial_data['author_difficulty'] = str(tutorial[6])
        tutorial_data['viewer_difficulty'] = str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = str(average_rating_type_for_tutorial('score', tutorial[0]))

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

@app.route('/api/tutorial/<username>/<tutorial_uuid>', methods=['GET'])
def get_one_tutorial(username, tutorial_uuid):

    sql_query = "SELECT * FROM diyup.tutorials WHERE author_username=%s AND uuid=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username, tutorial_uuid))
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s"
    cur.execute(sql_query, (tutorial[0],))
    steps = cur.fetchall()

    output_steps = []

    tutorial_data = {}
    tutorial_data['uuid'] = tutorial[0]
    tutorial_data['author_username'] = tutorial[1]
    tutorial_data['title'] = tutorial[2]
    tutorial_data['image'] = tutorial[3]
    tutorial_data['category'] = tutorial[4]
    tutorial_data['description'] = tutorial[5]
    tutorial_data['author_difficulty'] = str(tutorial[6])
    tutorial_data['viewer_difficulty'] = str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
    tutorial_data['rating'] = str(average_rating_type_for_tutorial('score', tutorial[0]))

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
    author_username = current_user[1]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO diyup.tutorials(uuid, title, image, category, description, author_difficulty, author_username) VALUES(%s, %s, %s, %s, %s, %s, %s)", (tutorial_uuid, title, image, category, description, float(author_difficulty), author_username))
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
    author_username = username

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diyup.users WHERE username=%s", (author_username,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user with that username exists.'})

    cur.execute("INSERT INTO diyup.tutorials(title, image, category, description, author_difficulty, author_username) VALUES(%s, %s, %s, %s, %s, %s)", (title, image, category, description, float(author_difficulty), author_username))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New tutorial created!'})

@app.route('/api/tutorial/<username>/<tutorial_uuid>', methods=['DELETE'])
@token_required
def delete_tutorial(current_user, username, tutorial_uuid):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot delete tutorial of a different user!'}), 403

    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid=%s AND author_username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, username,))
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'})

    sql_delete = "DELETE FROM diyup.tutorials WHERE uuid=%s AND author_username=%s"
    cur.execute(sql_delete, (tutorial_uuid, username,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Tutorial been deleted'})

######################
### STEP FUNCTIONS ###
######################

@app.route('/api/tutorial/<username>/<tutorial_uuid>/step', methods=['GET'])
def get_all_steps(tutorial_uuid, username):

    sql_query = "SELECT * FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s AND tutorials.author_username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, username,))
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

@app.route('/api/tutorial/<username>/<tutorial_uuid>/step/<step_index>', methods=['GET'])
def get_one_step(username, tutorial_uuid, step_index):

    sql_query = "SELECT * FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s AND tutorials.author_username=%s AND steps.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, username, step_index,))
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

@app.route('/api/tutorial/<username>/<tutorial_uuid>/step/create', methods=['POST'])
@token_required
def create_tutorial_step(current_user, username, tutorial_uuid):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot create tutorial for a different user!'}), 403

    data = request.get_json()

    cur = mysql.connection.cursor()

    index = cur.execute("SELECT COUNT(*) FROM diyup.steps WHERE diyup.steps.tutorial_uuid=%s", (tutorial_uuid,))

    # May get rid of later
    if index != 0:
        index += 1

    content = data['content']
    image = data['image']

    cur.execute("INSERT INTO diyup.steps(tutorial_uuid, steps.index, content, image) VALUES(%s, %s, %s, %s)", (tutorial_uuid, int(index), content, image,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been created'}, {'step id' : index})

@app.route('/api/tutorial/<username>/<tutorial_uuid>/step/<step_index>', methods=['DELETE'])
@token_required
def delete_tutorial_step(current_user, username, tutorial_uuid, step_index):
    if username != current_user[1] and current_user[3] == False:
        return jsonify({'message' : 'Cannot delete tutorial step for a different user!'}), 403

    sql_query = "SELECT * FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s AND tutorials.author_username=%s AND steps.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, username, step_index,))
    step = cur.fetchone()

    if not step:
        return jsonify({'message' : 'No step found for tutorial!'})

    sql_delete = "DELETE FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s AND tutorials.author_username=%s AND steps.index=%s"
    cur.execute(sql_query, (tutorial_uuid, username, step_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been deleted'})

########################
## COMMENTS FUNCTIONS ##
########################
@app.route('/api/tutorial/<username>/<tutorial_uuid>/comments/get_all', methods=['GET'])
def get_all_comments(username, tutorial_uuid):
    return ''

@app.route('/api/tutorial/<username>/<tutorial_uuid>/comments/get', methods=['GET'])
def get_comments(username, tutorial_uuid):
    return ''

@app.route('/api/tutorial/<username>/<tutorial_uuid>/comments/create', methods=['POST'])
@token_required
def create_tutorial_comment(current_user, username, tutorial_uuid):
    data = request.get_json()

    cur = mysql.connection.cursor()

    index = cur.execute("SELECT COUNT(*) FROM diyup.comments WHERE diyup.comments.tutorial_uuid=%s", (tutorial_uuid,))

    # May get rid of later
    if index != 0:
        index += 1

    return jsonify({'message' : 'Comment created!'}, {'comment id' : id})

######################
## RATING FUNCTIONs ##
######################
@app.route('/api/tutorial/<username>/<tutorial_id>/rate', methods=['POST'])
def user_rating(current_user, username, tutorial_id):
    return ''

# Helper method to get a tutorial's average ratings
def average_rating_type_for_tutorial(rating_type, tutorial_uuid):
    sql_query = "SELECT AVG(rating) FROM diyup.ratings WHERE rating_type=%s AND tutorial_uuid=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (rating_type, tutorial_uuid,))
    rating = cur.fetchone()
    return rating[0]

