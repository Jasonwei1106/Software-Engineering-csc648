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
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'}), 403

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
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'}), 403

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

    email_address = data['email_address']
    username = data['username']
    password = data['password']
    is_admin = '0'
    avatar = 'default.jpg'

    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.users WHERE email_address=%s OR username=%s", (email_address, username,))
    user = cur.fetchone()

    if user:
        if user[0] == email_address:
            return jsonify({'message' : 'Email already exists!'}), 400
        elif user[1] == username:
            return jsonify({'message' : 'Username already exists!'}), 400

    cur.execute("INSERT INTO diyup.users(email_address, username, password, is_admin, avatar) VALUES(%s, %s, %s, %s, %s)", (email_address, username, hashed_password, is_admin, avatar,))
    mysql.connection.commit()
    cur.close()

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
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'}), 403

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
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'}), 403

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
        return jsonify({'message' : 'Not an admin. Cannot perform that function!'}), 403

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

    return jsonify({'message' : 'User has been deleted!'})

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
        return make_response('Could not verify auth', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    sql_query = "SELECT * FROM diyup.users WHERE username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return make_response('Could not verify user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user[2], password):
        token = jwt.encode({'email_address' : user[0]}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'}
            )

@app.route('/api/user/forgot', methods=['POST'])
def forgot_password():

    data = request.get_json()

    email_address = data["email_address"]

    temporary_password = "(PLACEHOLDER)"

    if __name__ == '__main__':
        with app.app_context():
            msg = Message(
                subject="DIYup: Temporary Password",
                sender=app.config.get("MAIL_USERNAME"),
                recipients=[email_address],
                body="A request to reset a password for this user's DIYup account was made. Please use the temporary password \"%s\""
            )
            mail.send(msg)

    return jsonify({'message' : 'Temporary password has been sent!'})



@app.route('/api/user/<email_address>/reset', methods=['POST'])
@token_required
def reset_password(email_address):

    data = request.get_json()

    password = data['password']

    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    sql_update = "UPDATE diyup.users SET password=%s WHERE email_address=%s"
    cur.execute(sql_update, (hashed_password, email_address))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Password has been reset!'})
