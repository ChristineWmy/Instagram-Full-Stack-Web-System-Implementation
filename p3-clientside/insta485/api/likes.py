"""REST API for likes."""
import flask
import insta485
from insta485.api.util import error_checking, wrong_password, invalid_postid


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def create_likes():
    """Create likes for a specific post."""
    # Authentication
    if not flask.request.authorization and 'username' not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username_l = flask.session.get('username')
    else:
        username_l = flask.request.authorization['username']
        password_l = flask.request.authorization['password']
        # wrong password
        if wrong_password(username_l, password_l):
            return flask.jsonify(**error_checking(403)), 403

    # postid out of range
    postid = int(flask.request.args.get('postid'))
    if invalid_postid(postid):
        return flask.jsonify(**error_checking(404)), 404

    connection = insta485.model.get_db()

    # If likes already exist
    cur = connection.execute(
        "SELECT count(*) "
        "FROM likes "
        "WHERE owner = ? and postid = ?", (username_l, postid,))
    like_or_not = cur.fetchall()[0]['count(*)']
    if like_or_not:
        return flask.jsonify(**error_checking(409)), 409

    # Insert new like into database
    cur = connection.execute(
        "INSERT INTO "
        "likes(owner, postid) VALUES(?, ?)", (username_l, postid,))
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? and postid = ?", (username_l, postid,))
    likeid = cur.fetchall()[0]['likeid']
    context = {
        "likeid": likeid,
        "url": "/api/v1/likes/" + str(likeid) + "/"
    }
    # If insert success return 201 on success
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_likes(likeid):
    """Delete likes for a specific post, it is Ok to delete likes twice."""
    # Authentication
    if not flask.request.authorization and 'username' not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username_l = flask.session.get('username')
    else:
        username_l = flask.request.authorization['username']
        password_l = flask.request.authorization['password']
        # wrong password
        if wrong_password(username_l, password_l):
            return flask.jsonify(**error_checking(403)), 403

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT count(*) "
        "FROM likes "
        "WHERE likeid = ?", (likeid,))
    # like_or_not = cur.fetchall()[0]['count(*)']
    if len(cur.fetchall()) == 1:
        connection.execute(
            "DELETE FROM likes "
            "WHERE likeid = ?", (likeid,))
    context = {}
    return flask.jsonify(**context), 204
