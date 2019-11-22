from . import *

#####################
## ITEMS FUNCTIONS ##
#####################
@app.route('/api/items/<tutorial_uuid>/get', methods=['GET'])
def get_items(tutorial_uuid):

    sql_query = "SELECT * FROM diyup.items WHERE tutorial_uuid=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid,))
    items = cur.fetchall()
    cur.close()

    if not items:
        return jsonify({'message' : 'No items found!'}), 400

    output = []

    for item in items:
        item_data = {}
        item_data['tutorial_uuid'] = item[0]
        item_data['index'] = item[1]
        item_data['name'] = item[2]
        item_data['category'] = item[3]
        item_data['link'] = item[4]
        output.append(item_data)

    return jsonify({'items' : output}), 200

@app.route('/api/items/<tutorial_uuid>/create', methods=['POST'])
@token_required
def create_items(current_user, tutorial_uuid):

    data = request.get_json()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.items ORDER BY items.index DESC LIMIT 1")
    index = cur.fetchone()
    cur_index = int(index[1]) + 1

    name = data['name']
    category = data['category']
    link = data['link']

    cur.execute("INSERT INTO diyup.items(tutorial_uuid, items.index, name, category, link) VALUES(%s, %s, %s, %s, %s)", (tutorial_uuid, cur_index, name, category, link))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Item created!', 'item id' : cur_index}), 201

@app.route('/api/items/<tutorial_uuid>/<item_index>/delete', methods=['DELETE'])
@token_required
def delete_items(create_user, tutorial_uuid, item_index):

    sql_query = "SELECT * FROM diyup.items WHERE tutorial_uuid=%s AND items.index=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, item_index,))
    item = cur.fetchone()

    if not item:
        return jsonify({'message' : 'No item found!'})

    sql_delete = "DELETE FROM diyup.items WHERE items.index=%s"
    cur.execute(sql_delete, (item_index,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Item has been deleted!'})