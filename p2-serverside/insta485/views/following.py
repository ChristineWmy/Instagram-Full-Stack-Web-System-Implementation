"""
Insta485 following view.

URLs include:
/
"""
import flask
import insta485
from insta485.views.follow import follow_unfollow_request


@insta485.app.route('/users/<path:username>/following/',
                    methods=['POST', 'GET'])
def show_following(username):
    """Get details of following page and return template."""
    connection = insta485.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    cur = connection.execute(
        "SELECT username "
        "FROM users")
    userlist = []
    for user in cur.fetchall():
        userlist.append(user['username'])
    if username not in userlist:
        flask.abort(404)

    log_name = flask.session.get('username')
    if flask.request.method == 'POST':
        follow_unfollow_request()
    return show_followers_users(log_name, username)


def show_followers_users(logname, username):
    """Get details of following page and return template."""
    # Connect to database
    connection_ = insta485.model.get_db()

    cur = connection_.execute(
        "SELECT u.username, u.filename "
        "FROM following f "
        "JOIN users u "
        "on f.username2 = u.username "
        "WHERE f.username1 = ?", (username,))
    followers = cur.fetchall()

    user_followings = show_followers_users_details(logname, followers)

    context = {
        'username': username,
        'logname': logname,
        'following': user_followings
    }
    return flask.render_template('following.html', **context)


def show_followers_users_details(logname, followings):
    """Get details of following users."""
    connection = insta485.model.get_db()
    user_followings = []
    for following in followings:
        new_user_name = following['username']
        new_user_img_url = '/uploads/' + following['filename']
        cur = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE username1 = ? and username2 = ?", (logname, new_user_name,))
        logname_follows_username = (len(cur.fetchall()) == 1)
        follower_new = {
            'username': new_user_name,
            'user_img_url': new_user_img_url,
            'logname_follows_username': logname_follows_username}
        user_followings.append(follower_new)
    return user_followings
