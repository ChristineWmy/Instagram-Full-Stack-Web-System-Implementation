"""
Insta485 comments view.

URLs include:
/
"""
import flask
import insta485


def create_comments():
    """Insert comments."""
    ownername = flask.session.get('username')
    postid = flask.request.form['postid']
    text = flask.request.form['text']
    # if create an empty comment
    if len(text) <= 0:
        flask.abort(400)
    connection = insta485.model.get_db()
    connection.execute(
        "insert into comments (owner, postid, text) "
        "values(?, ?, ?)", (ownername, postid, text))


def delete_comments():
    """Delete comments."""
    logname = flask.session.get('username')
    comment_id = flask.request.form['commentid']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ?", (comment_id,))
    owner = cur.fetchall()[0]['owner']
    if owner != logname:
        flask.abort(403)
    connection.execute(
        "DELETE "
        "FROM comments "
        "WHERE commentid = ?", (comment_id,))


@insta485.app.route('/comments/', methods=["POST"])
def comments_request():
    """Display /comments/ route."""
    if flask.request.form.get('operation') == 'create':
        create_comments()
    elif flask.request.form.get('operation') == 'delete':
        delete_comments()
    if 'target' in flask.request.args:
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))
