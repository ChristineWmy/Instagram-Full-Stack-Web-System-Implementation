"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import arrow
import flask
from flask import send_from_directory
import insta485
# from insta485.views.likes import like_unlike_request


@insta485.app.route('/')
def show_index():
    """Display / route."""
    # flask.session['username'] = 'awdeorio'

    # Return to login page if not login
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session.get('username')

    # Connect to database
    connection = insta485.model.get_db()

    # Get followers for each user
    # print(type(logname))
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE following.username1 = ?", (logname,))
    users = cur.fetchall()

    # Append login user
    users.append({'username2': logname})

    # Initialize context
    context = {}

    new_user = []
    for user in users:
        new_user.append(user["username2"])
    # print(new_user)

    # print(tuple(new_user))

    if len(tuple(new_user)) == 1:
        cur = connection.execute(
            """ SELECT posts.postid, posts.owner,
                posts.filename AS `img_url`, posts.created AS `timestamp`,
                users.filename AS `owner_img_url`
                FROM posts
                JOIN users
                ON posts.owner = users.username AND users.username = ?
                ORDER BY posts.postid DESC;
            """, (tuple(new_user)[0], )
        )
    # Iterate Each follower
    # else:
    #     cur = connection.execute(
    #         "SELECT posts.postid, posts.owner, " +
    #         "posts.filename AS 'img_url', posts.created AS 'timestamp', " +
    #         "users.filename AS 'owner_img_url' " +
    #         "FROM posts " +
    #         "JOIN users " +
    #         "ON posts.owner = users.username AND users.username IN {} " +
    #         "ORDER BY posts.postid DESC"
    #         # .format(tuple(new_user))
    #     )

    posts = cur.fetchall()

    # add context
    context["posts"] = []
    for post in posts:
        post['timestamp'] = arrow.get(post['timestamp']).humanize()
        pid = post["postid"]
        owner = logname
        cur = connection.execute(
            "SELECT commentid, owner, text "
            "FROM comments "
            "WHERE comments.postid = ?", (pid,))
        comments = cur.fetchall()
        post["comments"] = comments

        cur = connection.execute(
            "SELECT COUNT(1) AS like_or_not "
            "FROM likes "
            "WHERE likes.postid = ? "
            "AND likes.owner = ?", (pid, owner,))
        post_like_or_not = cur.fetchall()
        post["like_or_not"] = post_like_or_not[0]["like_or_not"]

        # Get the number of likes of the post
        cur = connection.execute(
            "SELECT count(postid) as count_likes "
            "FROM likes "
            "WHERE postid = ?", (pid,))
        for like in cur:
            # print(like)
            post["likes"] = (like["count_likes"])

        context["posts"].append(post)

    context["logname"] = logname

    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Display /uploads/ route."""
    if 'username' not in flask.session:
        flask.abort(403)
    #     return flask.redirect(flask.url_for('login'))
    # connection = insta485.model.get_db()
    # print(filename)
    # cur = connection.execute(
    #     "SELECT username "
    #     "FROM users "
    #     "WHERE users.filename = ?", (filename, ))
    # result = cur.fetchall()
    # cur2 = connection.execute(
    #     "SELECT owner "
    #     "FROM posts "
    #     "WHERE posts.filename = ?", (filename, ))
    # result2 = cur2.fetchall()
    # print("result2:", result2, len(result2))
    if not os.path.isfile(insta485.app.config['UPLOAD_FOLDER'] / filename):
        flask.abort(404)
    # if len(result) != 0 & flask.session['username'] != result[0]['username']:
    #     flask.abort(403)
    # if len(result2) != 0 & flask.session['username'] != result2[0]['owner']:
    #     flask.abort(403)
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)
