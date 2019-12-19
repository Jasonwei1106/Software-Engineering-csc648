from . import *

######################
## RATING FUNCTIONS ##
######################
@app.route('/api/rate/<tutorial_uuid>/get_all', methods=['GET'])
def get_all_rating(tutorial_uuid):
    """
    Rating route to get all ratings

    Parameters
    ----------
    tutorial_uuid

    Returns
    -------
    Ratings

    """
    sql_query = "SELECT * FROM diyup.ratings WHERE tutorial_uuid=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid,))
    ratings = cur.fetchall()
    cur.close()

    if not ratings:
        return jsonify({'message' : 'No ratings found!'}), 400

    output = []

    for rating in ratings:
        rating_data = {}
        rating_data['tutorial_uuid'] = rating[0]
        rating_data['username'] = rating[1]
        rating_data['rating_type'] = rating[2]
        rating_data['rating'] = rating[3]
        output.append(rating_data)

    return jsonify({'ratings' : output}), 200

@app.route('/api/rate/<tutorial_uuid>/<rating_type>/get', methods=['GET'])
def get_rating(tutorial_uuid, rating_type,):
    """
    Rating route to get rating of specific type

    Parameters
    ----------
    tutorial_uuid, rating_type

    Returns
    -------
    Rating

    """
    sql_query = "SELECT * FROM diyup.ratings WHERE tutorial_uuid=%s \
        AND rating_type=%s"

    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, rating_type,))
    ratings = cur.fetchall()
    cur.close()

    if not ratings:
        return jsonify({'message' : 'No ratings found!'}), 400

    output = []

    for rating in ratings:
        rating_data = {}
        rating_data['tutorial_uuid'] = rating[0]
        rating_data['username'] = rating[1]
        rating_data['rating_type'] = rating[2]
        rating_data['rating'] = rating[3]
        output.append(rating_data)

    return jsonify({'ratings' : output}), 200

@app.route('/api/rate/<tutorial_uuid>/<rating_type>/create', methods=['POST'])
@token_required
def create_rating(current_user, tutorial_uuid, rating_type):
    """
    Rating route to create rating

    Parameters
    ----------
    Registered/Admin access, tutorial_uuid, rating_type

    Returns
    -------
    None

    """    
    data = request.get_json()

    rating = data['rating']

    cur = mysql.connection.cursor()

    cur.execute("REPLACE INTO diyup.ratings(tutorial_uuid, username, \
        ratings.rating_type, rating) VALUES(%s, %s, %s, %s)", \
        (tutorial_uuid, current_user[1], rating_type, float(rating),)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Rating has been created!'}), 201

@app.route('/api/rate/<tutorial_uuid>/<rating_type>/<username>/delete', \
    methods=['DELETE'])
@token_required
def delete_rating(current_user, tutorial_uuid, rating_type, username,):
    """
    Rating route to delete rating

    Parameters
    ----------
    Registered/Admin access, tutorial_uuid, rating_type, username

    Returns
    -------
    None

    """
    if current_user[3] == False:
        return jsonify({'message' : \
            'Cannot create tutorial for a different user!'}
        ), 403

    sql_query = "SELECT * FROM diyup.ratings WHERE tutorial_uuid=%s \
        AND username=%s AND rating_type=%s"

    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, username, rating_type,))
    rating = cur.fetchone()

    if not rating:
        return jsonify({'message' : 'No rating found!'}), 400

    sql_delete = "DELETE FROM diyup.ratings WHERE tutorial_uuid=%s \
        AND username=%s AND rating_type=%s"

    cur.execute(sql_delete, (tutorial_uuid, username, rating_type,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Rating has been deleted'}), 200
