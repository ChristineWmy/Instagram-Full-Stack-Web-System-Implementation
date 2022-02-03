"""
Insta485 follow view.

URLs include:
/following/
"""

import flask
import insta485


def follow(logname, username):
    """Follow function."""
    # username = "awdeorio"
    connection = insta485.model.get_db()
    connection.execute(
        'insert into following(username1, username2) values(?,?)',
        (logname, username,))


def unfollow(logname, username):
    """Unfollow function."""
    connection = insta485.model.get_db()
    connection.execute(
        'delete from following where username1 = ? and username2 = ?',
        (logname, username,))


@insta485.app.route('/following/', methods=["POST"])
def follow_unfollow_request():
    """Display /following/ route."""
    logname = flask.session.get('username')
    username = flask.request.form['username']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT count(*) as follow_or_not "
        "FROM following "
        "WHERE username1 = ? and username2 = ?", (logname, username))
    follow_or_not = cur.fetchall()
    if flask.request.form.get('operation') == 'follow':
        if follow_or_not[0]['follow_or_not'] != 0:
            flask.abort(409)
        follow(logname, username)

    elif flask.request.form.get('operation') == 'unfollow':
        if follow_or_not[0]['follow_or_not'] == 0:
            flask.abort(409)
        unfollow(logname, username)

    # return flask.redirect(flask.request.args.get("target"))
    if 'target' in flask.request.args:
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for("show_index"))
