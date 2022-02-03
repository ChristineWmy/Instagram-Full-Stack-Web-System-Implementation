"""
Insta485 users view.

URLs include:
/users/<username>/
"""
import flask
import insta485


@insta485.app.route('/users/<path:username>/', methods=['POST', 'GET'])
def show_user(username):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Connect to database
    connection = insta485.model.get_db()
    curr = connection.execute(
        "SELECT username "
        "FROM users")
    user_list = []
    for user in curr.fetchall():
        user_list.append(user['username'])
    if username not in user_list:
        flask.abort(404)
    logname = flask.session.get('username')
    return show_user_details(logname, username)


# @insta485.app.route('/users/<path: username>/', methods = ['POST', 'GET'])
def show_user_details(logname, username):
    """Display /users/username/ route."""
    # Connect to database
    connection = insta485.model.get_db()
    # Get full user name
    # print(username)
    cur = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ?", (username,))
    result = cur.fetchall()
    # print(result, len(result))

    if len(result) == 0:
        flask.abort(404)
    fullname = result[0]['fullname']
    # print(fullname)

    cur = connection.execute(
        "SELECT count(postid) as total_posts "
        "FROM posts "
        "WHERE owner = ?", (username,))
    total_posts = cur.fetchall()[0]['total_posts']

    cur = connection.execute(
        "SELECT count(username1) as followers "
        "FROM following "
        "WHERE username2 = ?", (username,))
    followers = cur.fetchall()[0]['followers']

    cur = connection.execute(
        "SELECT count(username2) as following "
        "FROM following "
        "WHERE username1 = ?", (username,))
    following = cur.fetchall()[0]['following']

    cur = connection.execute(
        "SELECT postid, filename "
        "FROM posts "
        "WHERE owner = ?", (username,))
    posts = cur.fetchall()
    # print(type(posts))
    new_posts = []
    for post in posts:
        img_url = "/uploads/" + post['filename']
        # print(img_url)
        new_posts.append({'postid': post['postid'], 'img_url': img_url})
        # print(post['postid'], post['filename'])

    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ? and username2 = ?", (logname, username,))
    # print(len(cur.fetchall())==1)
    logname_follows_username = (len(cur.fetchall()) == 1)
    # print(logname_follows_username)
    context = {
        "logname": logname,
        "username": username,
        "fullname": fullname,
        "followers": followers,
        "following": following,
        "total_posts": total_posts,
        "posts": new_posts,
        "logname_follows_username": logname_follows_username
    }
    # if flask.request.form.get('create_post') == 'upload new post':
    #     upload_files()
    return flask.render_template("users.html", **context)
