"""
Insta485 posts view.

URLs include:
/posts/
"""
import arrow
import flask
import insta485
# from insta485.views.likes import like_unlike_request


@insta485.app.route('/posts/<path:postid>/', methods=['POST', 'GET'])
def show_post(postid):
    """Display /posts/postid/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session.get('username')
    return show_post_details(logname, postid)


def show_post_details(logname, postid):
    """Get details of post page and return json string."""
    connection = insta485.model.get_db()

    # Get the image url, owner name and created timestamp for post
    cur = connection.execute(
        "SELECT filename as img_url, owner, created as timestamp "
        "FROM posts "
        "WHERE postid = ?", (postid,))
    info = cur.fetchall()[0]
    owner = info['owner']
    img_url = "/uploads/" + info['img_url']
    time = info['timestamp']
    timestamp = arrow.get(time).humanize()

    # Get the owner's image url of post
    cur = connection.execute(
        "SELECT filename as owner_img_url "
        "FROM users "
        "WHERE username = ?", (owner,))
    owner_img_url = '/uploads/' + cur.fetchall()[0]['owner_img_url']

    # Get the count of likes of post
    cur = connection.execute(
        "SELECT count(*) as likes "
        "FROM likes "
        "WHERE postid = ?", (postid,))
    likes = cur.fetchall()[0]['likes']

    # Get the comments of post with comments' owner and text
    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE postid = ?", (postid,))
    comments = cur.fetchall()

    # Whether the post is liked by login user
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE owner = ? and postid = ?", (logname, postid))
    post_like_or_not = (len(cur.fetchall()) == 1)
    # print(post_like_or_not)

    context = {
        "logname": logname,
        "postid": postid,
        "owner": owner,
        "owner_img_url": owner_img_url,
        "img_url": img_url,
        "timestamp": timestamp,
        "likes": likes,
        "comments": comments,
        "post_like_or_not": post_like_or_not
    }

    # print(context['comments'])

    return flask.render_template('post.html', **context)


@insta485.app.route('/posts/', methods=['POST'])
def delete_comments():
    """Display /posts/ route."""
    commentid = flask.request.form.get('commentid')
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE "
        "FROM comments "
        "WHERE commentid = ?", (commentid,))
    if 'target' in flask.request.args:
        return flask.redirect(flask.request.args.get("target"))
    return flask.redirect(flask.url_for('show_index'))


# @insta485.app.route('/posts/', methods=['POST'])
# def delete_posts():
#     """Display /posts/ route."""
#     postid = flask.request.form.get('postid')
#     # print(postid)
#     logname = flask.session.get('username')
#     # print(logname)
#     connection = insta485.model.get_db()
#     connection.execute(
#         "DELETE "
#         "FROM posts "
#         "WHERE postid = ?", (postid,))
#     if 'target' in flask.request.args:
#         return flask.redirect(flask.request.args.get("target"))
#     path = '/users/' + logname + '/'
#     return flask.redirect(path)
