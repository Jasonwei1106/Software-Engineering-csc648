from . import *

##########################
### TUTORIAL FUNCTIONS ###
##########################
@app.route('/api/tutorial/get', methods=['GET'])
def get_all_tutorials():
    """
    Tutorial route to get all tutorials

    Parameters
    ----------
    None

    Returns
    -------
    Tutorials

    """
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
        tutorial_data['viewer_difficulty'] = \
            str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = \
            str(average_rating_type_for_tutorial('score', tutorial[0]))
        output.append(tutorial_data)

    cur.close()

    return jsonify({'tutorials' : output}), 200

@app.route('/api/tutorial/get_all', methods=['GET'])
def get_all_tutorial_info():
    """
    Tutorial route to get tutorials with steps

    Parameters
    ----------
    None

    Returns
    -------
    Tutorials with steps

    """
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
        tutorial_data['viewer_difficulty'] = \
            str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = \
            str(average_rating_type_for_tutorial('score', tutorial[0]))

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

    return jsonify({'tutorials' : output}), 200

@app.route('/api/tutorial/<username>', methods=['GET'])
def get_all_tutorials_by_user(username):
    """
    Tutorial route to get all tutorials of a user

    Parameters
    ----------
    username

    Returns
    -------
    Tutorials

    """
    sql_query = "SELECT * FROM diyup.tutorials WHERE author_username=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (username,))
    tutorials = cur.fetchall()

    if not tutorials:
        return jsonify({'message' : 'No tutorial found!'}), 400

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
        tutorial_data['viewer_difficulty'] = \
            str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
        tutorial_data['rating'] = \
            str(average_rating_type_for_tutorial('score', tutorial[0]))

        for step in steps:
            step_data = {}
            step_data['index'] = step[1]
            step_data['content'] = step[2]
            step_data['image'] = step[3]
            output_steps.append(step_data)

        tutorial_data['steps'] = output_steps

        output.append(tutorial_data)

    cur.close()

    return jsonify({'tutorials' : output}), 200

@app.route('/api/tutorial/<tutorial_uuid>/get', methods=['GET'])
def get_one_tutorial(tutorial_uuid):
    """
    Tutorial route to get one tutorial of a user

    Parameters
    ----------
    tutorial_uuid

    Returns
    -------
    Tutorial

    """
    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid='{}'".format(
        tutorial_uuid
    )

    cur = mysql.connection.cursor()
    cur.execute(sql_query)
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'}), 400

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
    tutorial_data['viewer_difficulty'] = \
        str(average_rating_type_for_tutorial('difficulty', tutorial[0]))
    tutorial_data['rating'] = \
        str(average_rating_type_for_tutorial('score', tutorial[0]))

    for step in steps:
        step_data = {}
        step_data['index'] = step[1]
        step_data['content'] = step[2]
        step_data['image'] = step[3]
        output_steps.append(step_data)

    tutorial_data['steps'] = output_steps

    cur.close()

    return jsonify({'tutorial' : tutorial_data}), 200

@app.route('/api/tutorial/create', methods=['POST'])
@token_required
def create_tutorial(current_user):
    """
    Tutorial route to create tutorial

    Parameters
    ----------
    Registered/Admin access

    Returns
    -------
    Tutorial UUID

    """
    data = request.get_json()

    duplicate = True

    # To create new_set of UUID as a set
    # with open('api/tutorial_uuid_set.yaml', 'w') as uuid_file:
    #     new_set = set()
    #     yaml.dump(new_set, uuid_file)

    # Read the set of existing UUIDs
    with open('api/tutorial_uuid_set.yaml') as uuid_set_file:
        uuid_set = yaml.load(uuid_set_file)
        # Loop until a unique UUID is generated
        while duplicate is True:
            new_uuid = str(uuid.uuid4())
            if new_uuid not in uuid_set:
                duplicate = False

    with open('api/tutorial_uuid_set.yaml', 'w') as uuid_set_file:
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
    cur.execute("INSERT INTO diyup.tutorials(uuid, title, image, category, \
        description, author_difficulty, author_username) \
        VALUES(%s, %s, %s, %s, %s, %s, %s)", \
        (tutorial_uuid, title, image, category, description, \
        float(author_difficulty), author_username)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'New tutorial created!', \
        'token' : tutorial_uuid}
    ), 201

@app.route('/api/tutorial/<tutorial_uuid>', methods=['DELETE'])
@token_required
def delete_tutorial(current_user, tutorial_uuid):
    """
    Tutorial route to delete tutorial

    Parameters
    ----------
    Registered/Admin access, tutorial_uuid

    Returns
    -------
    None

    """
    cur = mysql.connection.cursor()

    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid=%s AND \
        author_username=%s"

    cur.execute(sql_query, (tutorial_uuid, current_user[1],))
    tutorial = cur.fetchone()

    if current_user[1] not in tutorial and current_user[3] == False:
        return jsonify({'message' : \
            'Permission denied!'}
        ), 401

    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid=%s AND \
        author_username=%s"

    author_username = tutorial[1]

    cur.execute(sql_query, (tutorial_uuid, author_username))
    tutorial = cur.fetchone()

    if not tutorial:
        return jsonify({'message' : 'No tutorial found!'}), 400

    sql_delete = "DELETE FROM diyup.tutorials WHERE uuid=%s AND \
        author_username=%s"

    cur.execute(sql_delete, (tutorial_uuid, author_username))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Tutorial been deleted'}), 200
