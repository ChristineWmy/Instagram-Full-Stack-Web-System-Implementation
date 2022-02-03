"""REST API for comments."""
import flask
import insta485
from insta485.api.util import error_checking, wrong_password, invalid_postid


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    """Create comments for a specific post."""
    # Authentication
    if not flask.request.authorization and 'username' not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username_c = flask.session.get('username')
    else:
        username_c = flask.request.authorization['username']
        password_c = flask.request.authorization['password']
        # wrong password
        if wrong_password(username_c, password_c):
            return flask.jsonify(**error_checking(403)), 403

    postid = int(flask.request.args.get('postid'))
    # postid out of range
    if invalid_postid(postid):
        return flask.jsonify(**error_checking(404)), 404

    text = flask.request.json["text"]
    connection = insta485.model.get_db()

    # Insert new comment into database
    cur = connection.execute(
        "INSERT INTO "
        "comments(owner, postid, text) VALUES(?, ?, ?)",
        (username_c, postid, text,))

    # Get basic information
    cur = connection.execute(
        "SELECT last_insert_rowid() as latest")
    latest_comment_id = cur.fetchall()[0]['latest']
    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE commentid = ?", (latest_comment_id,))
    info = cur.fetchall()[0]
    context = {
        "commentid": info['commentid'],
        "lognameOwnsThis": username_c == info['owner'],
        "owner": info['owner'],
        "ownerShowUrl": "/users/" + info['owner'] + "/",
        "text": info['text'],
        "url": "/api/v1/comments/" + str(info['commentid']) + "/",
    }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete comments for a specific post, it is Ok to delete likes twice."""
    # Authentication
    if not flask.request.authorization and 'username' not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username_c = flask.session.get('username')
    else:
        username_c = flask.request.authorization['username']
        password_c = flask.request.authorization['password']
        # wrong password
        if wrong_password(username_c, password_c):
            return flask.jsonify(**error_checking(403)), 403

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT count(*) "
        "FROM comments "
        "WHERE commentid = ?", (commentid,))
    if len(cur.fetchall()) == 1:
        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid = ?", (commentid,))
    context = {}
    return flask.jsonify(**context), 204
