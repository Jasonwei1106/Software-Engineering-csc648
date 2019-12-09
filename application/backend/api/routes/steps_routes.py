from . import *

######################
### STEP FUNCTIONS ###
######################

@app.route('/api/step/<tutorial_uuid>', methods=['GET'])
def get_all_steps(tutorial_uuid):
    """
    Step route to get all steps of a tutorial

    Parameters
    ----------
    tutorial_uuid

    Returns
    -------
    Steps

    """
    sql_query = "SELECT * FROM diyup.steps INNER JOIN diyup.tutorials \
        ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s"

    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid,))
    steps = cur.fetchall()
    cur.close()

    if not steps:
        return jsonify({'message' : 'No steps found for tutorial!'}), 400

    output = []

    for step in steps:
        step_data = {}
        step_data['tutorial_id'] = step[0]
        step_data['index'] = step[1]
        step_data['content'] = step[2]
        step_data['image'] = step[3]
        output.append(step_data)

    return jsonify({'steps' : output}), 200

@app.route('/api/step/<tutorial_uuid>/<step_index>', methods=['GET'])
def get_one_step(tutorial_uuid, step_index):
    """
    Step route to get one step

    Parameters
    ----------
    tutorial_uuid, step_index

    Returns
    -------
    Step

    """
    sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s \
        AND steps.index=%s"

    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, step_index,))
    step = cur.fetchone()
    cur.close()

    if not step:
        return jsonify({'message' : 'No steps found for tutorial!'}), 400

    step_data = {}
    step_data['tutorial_id'] = step[0]
    step_data['index'] = step[1]
    step_data['content'] = step[2]
    step_data['image'] = step[3]

    return jsonify({'steps' : step_data}), 200

@app.route('/api/step/<tutorial_uuid>/create', methods=['POST'])
@token_required
def create_tutorial_step(current_user, tutorial_uuid):
    """
    Step route to create step

    Parameters
    ----------
    Registered/Admin access, tutorial_uuid

    Returns
    -------
    Step ID

    """
    data = request.get_json()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.steps WHERE tutorial_uuid=%s \
        ORDER BY steps.index DESC LIMIT 1", (tutorial_uuid,)
    )
    index = cur.fetchone()

    if not index:
        cur_index = 1
    else:
        cur_index = int(index[1]) + 1

    indices = []

    content = data['content']
    image = data['image']

    if len(content) != len(image):
        return jsonify({'message': 'Arrays are not the same length!'}), 400

    for i in range(len(content)):
      cur.execute("INSERT INTO diyup.steps(tutorial_uuid, steps.index, \
          content, image) VALUES(%s, %s, %s, %s)", \
          (tutorial_uuid, cur_index, content[i], image[i],)
      )
      mysql.connection.commit()
      indices.append(cur_index)
      cur_index += 1

    cur.close()

    return jsonify({'message' : 'Step has been created', \
        'step id' : indices}
    ), 201

@app.route('/api/step/<tutorial_uuid>/<step_index>', methods=['DELETE'])
@token_required
def delete_tutorial_step(current_user, tutorial_uuid, step_index):
    """
    Step route to delete step

    Parameters
    ----------
    Registered/Admin access, tutorial_uuid, step_index

    Returns
    -------
    None

    """
    cur = mysql.connection.cursor()

    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid=%s \
        AND author_username=%s"

    cur.execute(sql_query, (tutorial_uuid, current_user[1],))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : \
            'Cannot delete tutorial step for a different user!'}
        ), 400
    elif current_user[3] == False:
        return jsonify({'message' : 'Not an admin!'}), 400

    sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s \
        AND steps.index=%s"

    cur.execute(sql_query, (tutorial_uuid, step_index,))
    step = cur.fetchone()

    if not step:
        return jsonify({'message' : 'No step found for tutorial!'}), 400

    sql_delete = "DELETE FROM diyup.steps INNER JOIN diyup.tutorials \
        ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s \
        AND steps.index=%s"

    cur.execute(sql_query, (tutorial_uuid, step_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been deleted'}), 200
