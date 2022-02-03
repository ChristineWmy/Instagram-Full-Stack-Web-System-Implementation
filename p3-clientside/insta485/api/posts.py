"""REST API for posts."""
import flask
import insta485
from insta485.api.util import error_checking, wrong_password
from insta485.api.post_info import get_post_info


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
    """Return post based on size, page, postid_lte."""
    # Authentication
    if not flask.request.authorization and "username" not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username = flask.session["username"]
    else:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        if wrong_password(username, password):
            return flask.jsonify(**error_checking(403)), 403

    # Set size and page, and check if size and page is larger than zero
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    if size < 0 or page < 0:
        return flask.jsonify(**error_checking(400)), 400

    connection = insta485.model.get_db()

    # Set postid_lte to the largest number of post if not defined
    post_latest = connection.execute(
        "SELECT postid FROM posts ORDER BY postid DESC LIMIT 1"
    ).fetchall()[0]
    postid_lte = flask.request.args.get("postid_lte",
                                        default=post_latest["postid"],
                                        type=int)

    cur = connection.execute(
        "SELECT postid FROM posts WHERE postid <= ? AND owner = ?"
        "OR postid <= ? AND owner IN "
        "(SELECT username2 FROM following WHERE username1 = ?) "
        "ORDER BY postid DESC LIMIT ? OFFSET ?",
        (postid_lte, username, postid_lte, username, size, size * page)
    )
    posts = cur.fetchall()

    # Get details of qualified posts
    context = {}
    post_ls = []
    for post in posts:
        postid_url_slug = post['postid']
        post_info = get_post_info(username, postid_url_slug)
        post_info['url'] = "/api/v1/posts/" + str(postid_url_slug) + "/"
        post_ls.append(post_info.copy())

    context["results"] = post_ls
    if ("size" in flask.request.args or "page" in flask.request.args or
            "postid_lte" in flask.request.args):
        context["url"] = flask.request.full_path
    else:
        context["url"] = flask.request.path

    # Check if there will be next page
    posts_all = connection.execute(
        "SELECT postid FROM posts WHERE postid <= ? AND owner = ?"
        "OR postid <= ? AND owner IN "
        "(SELECT username2 FROM following WHERE username1 = ?) "
        "ORDER BY postid DESC",
        (postid_lte, username, postid_lte, username)
    ).fetchall()

    if len(posts_all) >= size*(page+1):
        context["next"] = flask.request.path + "?size=" + str(size)\
            + "&page=" + str(page+1) + "&postid_lte=" + str(postid_lte)
        # "?size={}&page={}&postid_lte={}".format(size, page+1, postid_lte)
    else:
        context["next"] = ""

    return flask.jsonify(**context)
