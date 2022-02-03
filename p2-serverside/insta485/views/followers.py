"""
Insta485 follower view.

URLs include:
/
"""
import flask
import insta485
from insta485.views.follow import follow_unfollow_request


@insta485.app.route('/users/<path:username>/followers/',
                    methods=['GET', 'POST'])
def show_followers(username):
    """Show followers page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username "
        "FROM users")
    userslist = []
    for user in cur.fetchall():
        userslist.append(user['username'])
    if username not in userslist:
        flask.abort(404)

    logname = flask.session.get('username')
    if flask.request.method == 'POST':
        follow_unfollow_request()
    return show_followers_users(logname, username)


def show_followers_users(logname, username):
    """Get details of user page and return template."""
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT u.username, u.filename "
        "FROM following f "
        "JOIN users u "
        "on f.username1 = u.username "
        "WHERE f.username2 = ?", (username,))
    followers = cur.fetchall()
    user_followers = show_followers_users_details(logname, followers)
    # print(user_followers)
    # users = []
    context = {
        'username': username,
        'logname': logname,
        'followers': user_followers
    }
    return flask.render_template('followers.html', **context)


def show_followers_users_details(logname, followers):
    """Get details of follower users."""
    connection = insta485.model.get_db()
    user_followers = []
    for follower in followers:
        new_username = follower['username']
        new_user_img_url = '/uploads/' + follower['filename']

        cur = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE username1 = ? and username2 = ?", (logname, new_username,))
        logname_follows_username = (len(cur.fetchall()) == 1)

        follower_new = {
            'username': new_username,
            'user_img_url': new_user_img_url,
            'logname_follows_username': logname_follows_username}
        user_followers.append(follower_new)
    return user_followers
