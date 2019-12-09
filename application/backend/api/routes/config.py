from flask import request, jsonify, make_response
from flask_mail import Message
from api.config import app, db, mysql, mail
import yaml
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import time
from functools import wraps

# Token used to authenticate user
def token_required(f):
    """
    Home route to test frontend is connected to backend code.

    Attributes
    ----------

    Parameters
    ----------

    Returns
    -------

    """
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

####################
## HELPER METHODS ##
####################

# Helper method to get a tutorial's average ratings
def average_rating_type_for_tutorial(rating_type, tutorial_uuid):
    """
    Home route to test frontend is connected to backend code.

    Attributes
    ----------

    Parameters
    ----------

    Returns
    -------

    """
    sql_query = "SELECT AVG(rating) FROM diyup.ratings WHERE rating_type=%s \
        AND tutorial_uuid=%s"

    cur = mysql.connection.cursor()
    cur.execute(sql_query, (rating_type, tutorial_uuid,))
    rating = cur.fetchone()
    
    return rating[0]
