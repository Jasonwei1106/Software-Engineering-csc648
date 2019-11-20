from . import *

######################
### STEP FUNCTIONS ###
######################

@app.route('/api/step/<tutorial_uuid>', methods=['GET'])
def get_all_steps(tutorial_uuid):

    sql_query = "SELECT * FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s"
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

    sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s AND steps.index=%s"
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

    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diyup.steps ORDER BY steps.index DESC LIMIT 1")
    index = cur.fetchone()
    cur_index = int(index[0]) + 1

    content = data['content']
    image = data['image']

    cur.execute("INSERT INTO diyup.steps(tutorial_uuid, steps.index, content, image) VALUES(%s, %s, %s, %s)", (tutorial_uuid, cur_index, content, image,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been created', 'step id' : cur_index}), 201

@app.route('/api/step/<tutorial_uuid>/<step_index>', methods=['DELETE'])
@token_required
def delete_tutorial_step(current_user, tutorial_uuid, step_index):

    cur = mysql.connection.cursor()

    sql_query = "SELECT * FROM diyup.tutorials WHERE uuid=%s AND author_username=%s"
    cur.execute(sql_query, (tutorial_uuid, current_user[1],))
    user = cur.fetchone()

    if not user:
        return jsonify({'message' : 'Cannot delete tutorial step for a different user!'}), 400
    elif current_user[3] == False:
        return jsonify({'message' : 'Not an admin!'}), 400

    sql_query = "SELECT * FROM diyup.steps WHERE tutorial_uuid=%s AND steps.index=%s"
    cur.execute(sql_query, (tutorial_uuid, step_index,))
    step = cur.fetchone()

    if not step:
        return jsonify({'message' : 'No step found for tutorial!'}), 400

    sql_delete = "DELETE FROM diyup.steps INNER JOIN diyup.tutorials ON steps.tutorial_uuid = tutorials.uuid WHERE tutorials.uuid=%s AND steps.index=%s"
    cur.execute(sql_query, (tutorial_uuid, step_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Step has been deleted'})
