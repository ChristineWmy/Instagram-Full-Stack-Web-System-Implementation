"""
Insta485 likes view.

URLs include:
/likes/
"""

import flask
import insta485


def like():
    """Like function."""
    username = flask.session.get('username')
    postid = flask.request.form['postid']
    # Connect to database
    connection = insta485.model.get_db()
    # Add new like into database
    connection.execute(
        'insert into likes (owner, postid) values(?,?)',
        (username, postid))


def unlike():
    """Unlike function."""
    username = flask.session.get('username')
    postid = flask.request.form['postid']
    connection = insta485.model.get_db()
    connection.execute(
        'delete from likes where owner = ? and postid = ?',
        (username, postid))


@insta485.app.route('/likes/', methods=["POST"])
def like_unlike_request():
    """Display /likes/ route."""
    # Connect to database
    connection = insta485.model.get_db()
    pid = flask.request.form['postid']
    owner = flask.session['username']
    cur = connection.execute(
        "SELECT COUNT(1) AS like_or_not "
        "FROM likes "
        "WHERE likes.postid = (\"%s\") "
        "AND likes.owner = (\"%s\")" % (pid, owner))
    post_like_or_not = cur.fetchall()
    if flask.request.form.get('operation') == 'like':
        if post_like_or_not[0]["like_or_not"] != 0:
            flask.abort(409)
        like()
    elif flask.request.form.get('operation') == 'unlike':
        if post_like_or_not[0]["like_or_not"] == 0:
            flask.abort(409)
        unlike()
    return flask.redirect(flask.request.args.get("target"))
