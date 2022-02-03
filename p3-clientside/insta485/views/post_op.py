"""
Insta485 posts view.

URLs include:
/posts/
"""
import uuid
import pathlib
import os
import flask
import insta485


def upload_post(ownername):
    """Upload files."""
    # # ownername = 'awdeorio'
    # image = flask.request.files['file']
    # # print(image.filename)

    # filename = ''.join(random.sample(string.ascii_letters + string.digits,
    #     32))
    # full_filename = filename + '.' + image.filename.split('.')[1]
    # path = insta485.app.config['UPLOAD_FOLDER']/full_filename
    # image.save(path)

    # Unpack flask object
    fileobj = flask.request.files["file"]
    if fileobj is None:
        flask.abort(400)
    filename = fileobj.filename

    # Compute base name (filename without directory). We use a UUID
    # to avoid clashes with existing files, and ensure that the name
    # is compatible with the filesystem.

    uuid_basename = str(uuid.uuid4().hex) + \
        str(pathlib.Path(filename).suffix)

    # uuid_basename = "{stem}{suffix}".format(
    #     stem=uuid.uuid4().hex,
    #     suffix=pathlib.Path(filename).suffix
    # )

    # Save to disk
    path_ = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path_)

    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO posts(filename, owner)"
        "VALUES (?, ?)",
        (uuid_basename, ownername))


def delete_post():
    """Delete post."""
    postid = flask.request.form.get('postid')
    logname = flask.session.get('username')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename, owner "
        "FROM posts "
        "WHERE postid = ?", (postid,))
    result = cur.fetchall()
    owner = result[0]['owner']
    if owner != logname:
        flask.abort(403)
    file_path = insta485.app.config['UPLOAD_FOLDER'] / result[0]['filename']
    with open(file_path, encoding='ISO-8859-1', mode='r'):
        os.remove(file_path)
    # file_handle.close()
    connection.execute(
        "DELETE "
        "FROM posts "
        "WHERE postid = ?", (postid,))
    path = '/users/' + logname + '/'
    return path


@insta485.app.route('/posts/', methods=['POST'])
def create_delete_posts():
    """Display /posts/ route."""
    logname = flask.session.get('username')
    if flask.request.form.get('operation') == 'create':
        upload_post(logname)
        if 'target' in flask.request.args:
            return flask.redirect(flask.request.args.get('target'))
        path = '/users/' + logname + '/'
        # return flask.redirect(path)
    elif flask.request.form.get('operation') == 'delete':
        path = delete_post()
    return flask.redirect(path)
