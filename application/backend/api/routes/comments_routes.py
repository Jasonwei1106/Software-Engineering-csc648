""" Comment Routes

This file contains the comment routes.

This file is imported as a module and contains the following functions:
    * get_comments
    * get_all_comments
    * get_one_reply
    * create_tutorial_comment
    * reply_to_tutorial_comment
    * delete_comment

"""
from . import *

########################
## COMMENTS FUNCTIONS ##
########################
@app.route('/api/comments/get_all_comments', methods=['GET'])
def get_comments():
    """
    Comment route to get all comment information

    Parameters
    ----------
    None

    Returns
    -------
    Comments

    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diyup.comments")
    comments = cur.fetchall()
    cur.close()

    if not comments:
        return jsonify({'message' : 'No comments found.'}), 400

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

    return jsonify({'comments' : output}), 200

@app.route('/api/comments/<tutorial_uuid>/get_all', methods=['GET'])
def get_all_comments(tutorial_uuid):
    """
    Comment route to get comment information with 2 replies

    Parameters
    ----------
    tutorial_uuid

    Returns
    -------
    Comments with replies

    """
    sql_query = "SELECT * FROM diyup.comments WHERE tutorial_uuid=%s \
        AND reply_to IS null"

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
            reply_data['created'] = reply[4]
            reply_data['timestamp'] = reply[5]
            reply_data['edited'] = reply[6]
            reply_data['image'] = reply[7]
            reply_data['reply_to'] = reply[8]

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

    return jsonify({'comments' : output}), 200

@app.route('/api/comments/<tutorial_uuid>/<reply_to>', methods=['GET'])
def get_one_reply(tutorial_uuid, reply_to):
    """
    Comment route to get comment reply

    Parameters
    ----------
    tutorial_uuid, reply_to

    Returns
    -------
    Comment replies

    """
    sql_query = "SELECT * FROM diyup.comments WHERE tutorial_uuid=%s \
        AND reply_to=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (tutorial_uuid, reply_to,))
    replies = cur.fetchall()
    cur.close()

    if not replies:
        return jsonify({'message' : 'No replies found!'}), 400

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

    return jsonify({'replies' : output}), 200

@app.route('/api/comments/<tutorial_uuid>/create', methods=['POST'])
@token_required
def create_tutorial_comment(current_user, tutorial_uuid):
    """
    Comment route to create comment

    Parameters
    ----------
    Registered User access, tutorial_uuid

    Returns
    -------
    Comment ID

    """
    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diyup.tutorials WHERE uuid=%s", \
        (tutorial_uuid,))
    uuid = cur.fetchall()[0][0]

    if not uuid:
        return jsonify({'message' : 'No tutorial ID found!'}), 400

    cur.execute("SELECT * FROM diyup.comments ORDER BY id DESC LIMIT 1")
    index = cur.fetchone()

    content = data['content']
    image = data['image']
    edited = 0
    date = time.ctime()
    timestamp = date

    cur.execute("INSERT INTO diyup.comments(tutorial_uuid, username, \
        content, created, timestamp, edited, image) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)", \
        (tutorial_uuid, current_user[1], content, date, \
        timestamp, edited, image,)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Comment created!', \
        'comment id' : index[0]}), 201

@app.route('/api/comments/<tutorial_uuid>/create/<reply_id>', methods=['POST'])
@token_required
def reply_to_tutorial_comment(current_user, tutorial_uuid, reply_id):
    """
    Comment route to create comment reply

    Parameters
    ----------
    Registered/Admin User access, tutorial_uuid, reply_id

    Returns
    -------
    Comment ID

    """
    data = request.get_json()

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diyup.comments WHERE tutorial_uuid=%s AND \
        comments.id=%s", (tutorial_uuid, reply_id,)
    )

    uuid = cur.fetchone()

    if not uuid:
        return jsonify({'message' : 'No tutorial ID found!'}), 400

    cur.execute("SELECT * FROM diyup.comments ORDER BY id DESC LIMIT 1")
    index = cur.fetchone()
    id = int(index[0]) + 1

    content = data['content']
    image = data['image']
    reply_to = reply_id
    edited = 0
    date = time.ctime()
    timestamp = date

    cur.execute("INSERT INTO diyup.comments\
        (comments.tutorial_uuid, username, content, created, timestamp, \
        edited, image, reply_to) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
        (tutorial_uuid, current_user[1], content, date, timestamp, \
        edited, image, reply_to,)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Reply created!', 'comment id' : id}), 201

@app.route('/api/comments/delete/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    """
    Comment route to delete comment information

    Parameters
    ----------
    Registered/Admin User access, comment_id

    Returns
    -------
    None

    """
    sql_query = "SELECT * FROM diyup.comments WHERE comments.id=%s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (comment_id,))
    comment = cur.fetchone()

    if not comment:
        return jsonify({'message' : 'No comment found!'}), 400
    elif current_user[3] == False:
        return jsonify({'message' : 'Not an admin!'}), 400

    sql_delete = "DELETE FROM diyup.comments WHERE comments.id=%s"
    cur.execute(sql_delete, (comment_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message' : 'Comment deleted'}), 200
