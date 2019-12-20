from . import *

######################
### USER FUNCTIONS ###
######################

@app.route('/api/user/get', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    User route to get all user

    Parameters
    ----------
    Admin access

    Returns
    -------
    User Data

    """
    if current_user[3] != True:
        return jsonify({'message' : \
            'Not an admin. Cannot perform that function!'}
        ), 403

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

    return jsonify({'users' : output}), 200

@app.route('/api/user/<email_address>', methods=['GET'])
@token_required
def get_one_user(current_user, email_address):
    """
    User route to get one user

    Parameters
    ----------
    Registered/Admin access, email_address

    Returns
    -------
    User Data

    """
    if current_user[3] != True:
        return jsonify({'message' : \
            'Not an admin. Cannot perform that function!'}
        ), 403

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    user_data = {}
    user_data['email_address'] = user[0]
    user_data['username'] = user[1]
    user_data['password'] = user[2]
    user_data['is_admin'] = user[3]
    user_data['avatar'] = user[4]

    return jsonify({'users' : user_data}), 200

@app.route('/api/user/current_user', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    User route to get current user

    Parameters
    ----------
    Registered/Admin access

    Returns
    -------
    User Data

    """
    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (current_user[0],))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    user_data = {}
    user_data['email_address'] = current_user[0]
    user_data['username'] = current_user[1]
    user_data['is_admin'] = current_user[3]
    user_data['password'] = '****'
    user_data['avatar'] = current_user[4]

    return jsonify({'current user' : user_data}), 200

@app.route('/api/user/create', methods=['POST'])
def create_user():
    """
    User route to create user

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    data = request.get_json()

    duplicate = True

    # To create new_set of UUID as a set
    # with open('api/user_uuid_set.yaml', 'w') as uuid_file:
    #     new_set = set()
    #     yaml.dump(new_set, uuid_file)

    # Read the set of existing UUIDs
    with open('api/user_uuid_set.yaml') as uuid_set_file:
        uuid_set = yaml.load(uuid_set_file)
        # Loop until a unique UUID is generated
        while duplicate is True:
            new_uuid = str(uuid.uuid4())
            if new_uuid not in uuid_set:
                duplicate = False

    with open('api/user_uuid_set.yaml', 'w') as uuid_set_file:
        # Add the new UUID to the set and dump it to the file
        uuid_set.add(new_uuid)
        yaml.dump(uuid_set, uuid_set_file)

    user_uuid = new_uuid
    email_address = data['email_address']
    username = data['username']
    password = data['password']
    is_admin = '0'
    avatar = 'default.jpg'

    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.users WHERE email_address=%s OR \
        username=%s", (email_address, username,)
    )

    user = cur.fetchone()

    if user:
        if user[0] == email_address:
            return jsonify({'message' : 'Email already exists!'}), 400
        elif user[1] == username:
            return jsonify({'message' : 'Username already exists!'}), 400

    cur.execute("INSERT INTO diyup.users(email_address, username, \
        password, is_admin, avatar, uuid) \
        VALUES(%s, %s, %s, %s, %s, %s)", \
        (email_address, username, hashed_password, is_admin, avatar, user_uuid)
    )

    mysql.connection.commit()
    cur.close()

    verification_url = "http://54.67.109.241:5000/api/user/%s/verify/%s" % \
        (username, user_uuid)

    with app.app_context():
        msg = Message(
            subject="DIYup: Email Address Verification",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[email_address],
            body="Hello %s, welcome to DIYup! Please click on this link to\n"
                "verify your email address: %s\n\n" 
                "If you did not sign up for an account, feel free to\n"
                "ignore this email.\n\n"
                "- DIYup Administration" % (username, verification_url)
        )
        mail.send(msg)

    return jsonify({'message' : 'New user created!'}), 201

@app.route('/api/user/<email_address>/promote', methods=['PUT'])
@token_required
def promote_user(current_user, email_address):
    """
    User route to promote user

    Parameters
    ----------
    Admin access, email_address

    Returns
    -------
    None

    """
    if current_user[3] != True:
        return jsonify({'message' : \
            'Not an admin. Cannot perform that function!'}
        ), 403

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'}), 400

    sql_update = "UPDATE diyup.users SET is_admin = 1 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been promoted!'}), 201

@app.route('/api/user/<email_address>/demote', methods=['PUT'])
@token_required
def demote_user(current_user, email_address):
    """
    User route to demote user

    Parameters
    ----------
    Admin access, email_address

    Returns
    -------
    None

    """
    if current_user[3] != True:
        return jsonify({'message' : \
            'Not an admin. Cannot perform that function!'}
        ), 403

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'}), 400

    sql_update = "UPDATE diyup.users SET is_admin = 0 WHERE email_address=%s"
    cur.execute(sql_update, (email_address,))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been demoted!'}), 201

@app.route('/api/user/<email_address>', methods=['DELETE'])
@token_required
def delete_user(current_user, email_address):
    """
    User route to delete user

    Parameters
    ----------
    Admin access, email_address

    Returns
    -------
    None

    """
    if current_user[3] != True:
        return jsonify({'message' : \
            'Not an admin. Cannot perform that function!'}
        ), 403

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'No user found!'}), 400

    sql_delete = "DELETE FROM diyup.users WHERE email_address=%s"
    cur.execute(sql_delete, (email_address,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'User has been deleted!'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    """
    User route to login

    Parameters
    ----------
    None

    Returns
    -------
    Token

    """
    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username:
        return make_response('Could not verify auth',\
            401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}
        )

    sql_query = "SELECT * FROM diyup.users WHERE username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return make_response('Could not verify user', \
            401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}
        )

    if check_password_hash(user[2], password):
        token = jwt.encode({'email_address' : user[0]}, \
            app.config['SECRET_KEY']
        )

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', \
        401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}
    )

@app.route('/api/user/verify/<username>/<user_uuid>', methods=['POST'])
def verify_user(username, user_uuid):

    """
    User route to verify a user's email address

    Parameters
    ----------
    username, user_uuid

    Returns
    -------
    None

    """

    sql_query = "SELECT uuid FROM diyup.users WHERE username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    real_user_uuid = cur.fetchall()[0][0]
    print(real_user_uuid)
    print(user_uuid)

    if user_uuid == real_user_uuid:
        sql_update = "UPDATE diyup.users SET is_verified=1 WHERE \
            username=%s"
        cur.execute(sql_update, (username,))
        cur.close()
        return redirect("http://54.67.109.241", code=302)
    else:
        cur.close()
        return jsonify({'message' : \
            'User verification link does not exist.'}
        ), 404


@app.route('/api/user/forgot/send', methods=['POST'])
def send_password_reset_code():

    """
    User route to email user a password reset code

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    data = request.get_json()

    email_address = data["email_address"]

    password_reset_code = str(uuid.uuid4())

    cur = mysql.connection.cursor()
    sql_update = "UPDATE diyup.users SET password_reset_code=%s WHERE \
        email_address=%s"
    cur.execute(sql_update, (password_reset_code, email_address,))
    mysql.connection.commit()
    cur.close()

    with app.app_context():
        msg = Message(
            subject="DIYup: Password Reset",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[email_address],
            body="A request to reset a password for this user's DIYup\n"
                " account was made. Please use the password reset code \n"
                "\"%s\"\n\n" 
                "- DIYup Administration"% password_reset_code
        )
        mail.send(msg)

    return jsonify({'message' : 'Password reset code has been sent!'}), 200

@app.route('/api/user/forgot/verify', methods=['POST'])
def verify_password_reset_code():

    """
    User route to verify a user's password reset code

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    data = request.get_json()

    email_address = data["email_address"]
    password_reset_code = data["password_reset_code"]

    sql_query = "SELECT * FROM diyup.users WHERE email_address=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (email_address,))
    user = cur.fetchone()
    cur.close()

    if user[7] == password_reset_code:
        return jsonify({'message' : 'Password reset code is valid!'}), 200
    else:
        return jsonify({'message' : 'Password reset code is not valid.'}), 400



@app.route('/api/user/forgot/reset', methods=['POST'])
def reset_password():

    """
    User route to reset a user's password

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    data = request.get_json()

    email_address = data['email_address']
    new_password = data['password']

    hashed_password = generate_password_hash(new_password, method='sha256')

    cur = mysql.connection.cursor()

    sql_update = "UPDATE diyup.users SET password=%s WHERE email_address=%s"
    cur.execute(sql_update, (hashed_password, email_address,))
    mysql.connection.commit()

    sql_update = "UPDATE diyup.users SET password_reset_code=%s WHERE \
        email_address=%s"
    cur.execute(sql_update, (None, email_address,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Password has been reset!'}), 200
