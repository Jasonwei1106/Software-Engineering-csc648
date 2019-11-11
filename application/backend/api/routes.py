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
    cur.execute("SELECT * FROM team206.users WHERE email_address=%s OR username=%s", (email_address, username,))
    user = cur.fetchone()

    if user:
        if user[0] == email_address:
            return jsonify({'message' : 'Email already exists!'}), 400
        elif user[1] == username:
            return jsonify({'message' : 'Username already exists!'}), 400
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
        # token = jwt.encode({'email_address' : user[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        token = jwt.encode({'email_address' : user[0]}, app.config['SECRET_KEY'])
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

    return jsonify({'tutorials' : output})

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

@app.route('/api/tutorial/<username>/<tutorial_id>', methods=['DELETE'])
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
# Get all comments
@app.route('/api/comments/get_all_comments', methods=['GET'])
def get_comments():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.comments")
    comments = cur.fetchall()
    cur.close()

    if not comments:
        return jsonify({'message' : 'No comments found.'})

    output = []

    for comment in comments:
        comment_data = {}
        comment_data['id'] = comment[0]
        comment_data['tutorial_uuid'] = comment[1]
        comment_data['username'] = comment[2]
        comment_data['content'] = comment[3]
        comment_data['created'] = comment[4]
        comment_data['timestamp'] = comment[5]
        comment_data['edited'] = comment[6]
        comment_data['image'] = comment[7]
        comment_data['reply_to'] = comment[8]
        output.append(comment_data)

    return jsonify({'comments' : output})

# Return comments + 2 children
@app.route('/api/comments/<tutorial_uuid>/get_all', methods=['GET'])
def get_all_comments(tutorial_uuid):

    sql_query = "SELECT * FROM diyup.comments WHERE tutorial_uuid=%s AND reply_to IS null"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid,))
    comments = cur.fetchall()

    output = []

    for comment in comments:
        sql_query = "SELECT * FROM diyup.comments WHERE reply_to=%s"
        cur.execute(sql_query, (comment[0],))
        replys = cur.fetchall()

        output_reply = []

        comment_data = {}
        comment_data['id'] = comment[0]
        comment_data['tutorial_uuid'] = comment[1]
        comment_data['username'] = comment[2]
        comment_data['content'] = comment[3]
        comment_data['created'] = comment[4]
        comment_data['timestamp'] = comment[5]
        comment_data['edited'] = comment[6]
        comment_data['image'] = comment[7]
        comment_data['reply_to'] = comment[8]

        for reply in replys:
            reply_data = {}
            reply_data['id'] = reply[0]
            reply_data['username'] = reply[2]
            reply_data['content'] = reply[3]
            reply_data['image'] = reply[4]
            reply_data['reply_to'] = reply[5]
            reply_data['edited'] = reply[6]

            sql_query = "SELECT * FROM diyup.comments WHERE reply_to=%s"
            cur.execute(sql_query, (reply[0],))
            replies_to = cur.fetchall()

            output_reply_reply = []

            for r in replies_to:
                r_data = {}
                r_data['id'] = r[0]
                r_data['username'] = r[2]
                r_data['content'] = r[3]
                r_data['image'] = r[4]
                r_data['reply_to'] = r[5]
                r_data['edited'] = r[6]
                output_reply_reply.append(r_data)

            reply_data['child reply'] = output_reply_reply
            output_reply.append(reply_data)

        comment_data['replies'] = output_reply

        output.append(comment_data)

    cur.close()

    return jsonify({'comments' : output})

# Get reply of a comment based off comment id
@app.route('/api/comments/<tutorial_uuid>/<reply_to>', methods=['GET'])
def get_one_reply(tutorial_uuid, reply_to):

    sql_query = "SELECT * FROM diyup.comments WHERE tutorial_uuid=%s AND reply_to=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, reply_to,))
    replies = cur.fetchall()
    cur.close()

    if not replies:
        return jsonify({'message' : 'No replies found!'})

    output = []

    for reply in replies:
        reply_data = {}
        reply_data['id'] = reply[0]
        reply_data['tutorial_uuid'] = reply[1]
        reply_data['username'] = reply[2]
        reply_data['content'] = reply[3]
        reply_data['image'] = reply[4]
        reply_data['reply_to'] = reply[5]
        reply_data['edited'] = reply[6]
        output.append(reply_data)

    return jsonify({'replies' : output})

@app.route('/api/comments/<tutorial_uuid>/create', methods=['POST'])
@token_required
def create_tutorial_comment(current_user, tutorial_uuid):
    data = request.get_json()

    cur = mysql.connection.cursor()

    uuid = cur.execute("SELECT * FROM diyup.comments WHERE tutorial_uuid=%s", (tutorial_uuid,))

    if not uuid:
        return jsonify({'message' : 'No tutorial ID found!'})

    cur.execute("SELECT * FROM diyup.comments ORDER BY id DESC LIMIT 1")
    index = cur.fetchone()

    content = data['content']
    image = data['image']
    edited = 0

    cur.execute("INSERT INTO diyup.comments(comments.tutorial_uuid, username, content, image, edited)", (tutorial_uuid, current_user[1], content, image, edited,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Comment created!'}, {'comment id' : index[0]})

@app.route('/api/comments/<tutorial_uuid>/create/<reply_comment_id>', methods=['POST'])
@token_required
def reply_to_tutorial_comment(current_user, tutorial_uuid, comment_id):
    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diyup.comments WHERE tutorial_uuid=%s", (tutorial_uuid,))
    uuid = cur.fetchall()

    if not uuid:
        return jsonify({'message' : 'No tutorial ID found!'})

    cur.execute("SELECT * FROM diyup.comments ORDER BY id DESC LIMIT 1")
    index = cur.fetchone()

    content = data['content']
    image = data['image']
    reply_to = comment_id
    edited = 0

    cur.execute("INSERT INTO diyup.comments(comments.tutorial_uuid, username, content, image, reply_to, edited)", (tutorial_uuid, current_user[1], content, image, reply_to, edited,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Reply created!'}, {'comment id' : index[0]})

@app.route('/api/comments/delete/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    # if username != current_user[1] and current_user[3] == False:
    #     return jsonify({'message' : 'Cannot delete comment for a different user!'}), 403

    sql_query = "SELECT * FROM diyup.comments WHERE comments.id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (comment_id,))
    comment = cur.fetchone()

    if not comment:
        return jsonify({'message' : 'No comment found!'})

    sql_delete = "DELETE FROM diyup.comments WHERE comments.id=%s"
    cur.execute(sql_delete, (comment_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Comment deleted'})

#####################
## ITEMS FUNCTIONS ##
#####################
@app.route('/api/items/<tutorial_uuid>/get', methods=['GET'])
def get_items(tutorial_uuid):

    sql_query = "SELECT * FROM diyup.items WHERE tutorial_uuid=%s"
    cur = mysl.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid,))
    items = cur.fetchall()
    cur.close()

    if not items:
        return jsonify({'message' : 'No items found!'})

    output = []

    for item in items:
        item_data = {}
        item_data['tutorial_uuid'] = item[0]
        item_data['index'] = item[1]
        item_data['name'] = item[2]
        item_data['category'] = item[3]
        item_data['link'] = item[4]
        output.append(item_data)

    return jsonify({'items' : output})

@app.route('/api/items/<tutorial_uuid>/create', methods=['POST'])
def create_items(tutorial_uuid):

    data = request.get_json()


    index = cur.execute("SELECT COUNT(*) FROM diyup.items WHERE tutorial_uuid=%s", (tutorial_uuid,))

    if index != 0:
        index += 1

    name = data['name']
    category = data['category']

    if data['link']:
        link = data['link']

    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO diyup.items(tutorial_uuid, items.index, name, category, link) VALUES(%s, %s, %s, %s, %s)", (tutorial_uuid, int(index), name, category, link))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Item created!'}, {'item id' : index})

@app.route('/api/items/<tutorial_uuid>/<item_index>/delete', methods=['DELETE'])
def delete_items(tutorial_uuid, item_index):
    # if username != current_user[1] and current_user[3] == False:
    #     return jsonify({'message' : 'Cannot delete tutorial step for a different user!'}), 403

    sql_query = "SELECT * FROM diyup.items WHERE tutorial_uuid=%s AND items.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, item_index,))
    item = cur.fetchone()

    if not item:
        return jsonify({'message' : 'No item found!'})

    sql_delete = "DELETE FROM diyup.items WHERE itesm.index=%s"
    cur.execute(sql_delete, (item_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Item has been deleted!'})

######################
## RATING FUNCTIONS ##
######################
@app.route('/api/rate/<tutorial_uuid>', methods=['POST'])
def user_rating(username, tutorial_uuid):
    return ''

# Helper method to get a tutorial's average ratings
def average_rating_type_for_tutorial(rating_type, tutorial_uuid):
    sql_query = "SELECT AVG(rating) FROM diyup.ratings WHERE rating_type=%s AND tutorial_uuid=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (rating_type, tutorial_uuid,))
    rating = cur.fetchone()
    return rating[0]
