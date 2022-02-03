"""
Insta485 accounts (main) view.

URLs include:
/
"""
import pathlib
import uuid
import hashlib
import os
import flask
import insta485


@insta485.app.route('/accounts/login/')
def login():
    """Login."""
    # Return to the index page if already logged in.
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    context = {}
    return flask.render_template("login.html", **context)


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Logout."""
    if 'username' in flask.session:
        flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/create/')
def create():
    """Create."""
    # Return to the index page if already logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    context = {}
    return flask.render_template("create.html", **context)


@insta485.app.route('/accounts/delete/')
def delete():
    """Delete."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    username_c = flask.session['username']
    context = {'username': username_c}
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/')
def edit():
    """Edit."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, fullname, email, filename "
        "FROM users "
        "WHERE users.username = ?",
        (flask.session['username'], )
    )
    current = cur.fetchall()
    context = {
        'logname': current[0]['username'],
        'fullname': current[0]['fullname'],
        'email': current[0]['email'],
        "img_url": '/uploads/' + current[0]['filename']
    }
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/')
def password_():
    """Password."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # username_c = flask.session['username']
    # password_c = flask.session['new_password1']
    # connection = insta485.model.get_db()
    #
    # cur = connection.execute(
    #     "UPDATE users "
    #     "SET password = ? "
    #     "WHERE users.username = ?",
    #     (password_c, username_c)
    # )
    # connection = insta485.model.get_db()
    logname = flask.session.get('username')
    context = {
        'logname': logname
    }
    return flask.render_template("password.html", **context)


def create_op():
    """Create operation."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')

    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    if (not username or not password or not fullname
       or not email or not fileobj):
        flask.abort(400)
    if filename == '':
        flask.abort(400)

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT COUNT(1) AS exist_or_not "
        "FROM users "
        "WHERE users.username = ?", (username, ))

    uses = cur.fetchall()
    if uses[0]['exist_or_not'] != 0:
        flask.abort(409)

    # Compute base name (filename without directory).
    # We use a UUID to avoid clashes with existing files,
    # and ensure that the name is compatible with the filesystem.
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    # print(uuid_basename)

    # Generate Password
    # algorithm = 'sha512'
    # salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = uuid.uuid4().hex + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', uuid.uuid4().hex, password_hash])

    cur = connection.execute(
        """ INSERT INTO users(username, fullname, email, filename, password)
            VALUES (?, ?, ?, ?, ?)""",
        (username, fullname, email, uuid_basename, password_db_string))
    flask.session['username'] = username


def delete_op():
    """Delete operation."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        flask.abort(403)
    # Connect to database
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE users.username = ?",
        (flask.session['username'], )
    )
    result = cur.fetchall()
    filepath = insta485.app.config['UPLOAD_FOLDER'] / result[0]['filename']
    with open(filepath, encoding='ISO-8859-1', mode='r'):
        os.remove(filepath)

    # file_handle.close()

    cur = connection.execute(
        "SELECT filename  "
        "FROM posts "
        "WHERE posts.owner = ?",
        (flask.session['username'], )
    )
    files = cur.fetchall()
    for file in files:
        filepath = insta485.app.config['UPLOAD_FOLDER'] / file['filename']
        with open(filepath, encoding='ISO-8859-1', mode='r'):
            os.remove(filepath)
        # file_handle.close()

    # Check if users in database
    cur = connection.execute(
        "DELETE FROM users "
        "WHERE users.username = ?",
        (flask.session['username'], )
    )
    flask.session.clear()


def edit_op():
    """Edit operation."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        flask.abort(403)
    # Connect to database
    connection = insta485.model.get_db()

    # Check if users in database
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')

    # Need to add file
    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    if filename != '':
        # Compute base name (filename without directory).
        # We use a UUID to avoid clashes with existing files,
        # and ensure that the name is compatible with the filesystem.
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
        )

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

    if not fullname or not email:
        flask.abort(400)

    connection = insta485.model.get_db()
    connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ? "
        "WHERE users.username = ?",
        (fullname, email, flask.session['username'])
    )
    if filename != '':
        connection.execute(
            "UPDATE users "
            "SET filename = ? "
            "WHERE users.username = ?",
            (uuid_basename, flask.session['username'])
        )


def password_op():
    """Password operation."""
    # Return to the index page if already logged in
    if 'username' not in flask.session:
        flask.abort(403)

    password = flask.request.form.get('password')
    new_password1 = flask.request.form.get('new_password1')
    new_password2 = flask.request.form.get('new_password2')

    if not password or not new_password1 or not new_password2:
        flask.abort(400)

    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE users.username = ?",
        (flask.session['username'], )
    )
    pas = cur.fetchall()

    salt = pas[0]['password'].split('$')[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    # Check if users in database
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE users.username = ?",
        (flask.session['username'], )
    )
    current = cur.fetchall()

    if password_db_string != current[0]['password']:
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)

    # Generate Password
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    print(flask.session['username'], new_password1)
    cur = connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE users.username = ?",
        (password_db_string, flask.session['username'])
    )


@insta485.app.route('/accounts/', methods=['POST'])
def accounts_operation():
    """Account operation."""
    if flask.request.form.get('operation') == 'login':
        # Connect to database
        connection = insta485.model.get_db()

        # Get the submitted username and password
        username_s = flask.request.form.get('username')
        password_s = flask.request.form.get('password')

        # Check if the string is empty or NOT
        if username_s == '' or password_s == '':
            flask.abort(400)

        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE users.username = ?",
            (username_s, )
        )
        pas = cur.fetchall()
        if len(pas) == 0:
            flask.abort(403)
        salt = pas[0]['password'].split('$')[1]
        algorithm = 'sha512'
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password_s
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Check if users in database
        cur = connection.execute(
            "SELECT 1 "
            "FROM users "
            "WHERE users.username = ? AND users.password = ?",
            (username_s, password_db_string)
        )
        result = cur.fetchall()
        if len(result) == 0:
            flask.abort(403)
        flask.session['username'] = username_s
    elif flask.request.form.get('operation') == 'delete':
        delete_op()
    elif flask.request.form.get('operation') == 'edit_account':
        edit_op()
    elif flask.request.form.get('operation') == 'create':
        create_op()
    elif flask.request.form.get('operation') == 'update_password':
        password_op()

    if 'target' in flask.request.args:
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))
