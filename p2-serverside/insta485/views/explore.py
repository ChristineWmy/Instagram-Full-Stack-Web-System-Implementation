"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Show explore page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session.get('username')
    return show_explore_details(logname)


def show_explore_details(logname):
    """Get details of explore page and return template."""
    # logname = flask.session.get('username')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT u.username "
        "FROM users u "
        "WHERE u.username != ? and u.username not in "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ?)", (logname, logname))
    # print(cur.fetchall())
    unfollowing = cur.fetchall()
    unfollow_details = []
    for unfollow in unfollowing:
        unfollow_name = unfollow['username']
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?", (unfollow_name,))
        filename = cur.fetchall()[0]['filename']
        unfollow_filename = '/uploads/' + filename
        unfollow_details.append({
            "username": unfollow_name,
            "user_img_url": unfollow_filename
            })
    context = {
        "logname": logname,
        "not_following": unfollow_details
    }
    return flask.render_template('explore.html', **context)
