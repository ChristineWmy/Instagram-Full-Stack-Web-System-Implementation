"""REST API for post."""
import flask
import insta485
from insta485.api.util import error_checking, wrong_password, invalid_postid
from insta485.api.post_info import get_post_info


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['GET'])
def get_post(postid_url_slug):
    """Return post on postid_url_slug."""
    # Authentication
    if not flask.request.authorization and "username" not in flask.session:
        return flask.jsonify(**error_checking(403)), 403
    if not flask.request.authorization:
        username_p = flask.session.get('username')
    else:
        username_p = flask.request.authorization['username']
        password_p = flask.request.authorization['password']
        # wrong password
        if wrong_password(username_p, password_p):
            return flask.jsonify(**error_checking(403)), 403

    # postid out of range
    if invalid_postid(postid_url_slug):
        return flask.jsonify(**error_checking(404)), 404

    context = get_post_info(username_p, postid_url_slug)
    context['url'] = flask.request.path
    return flask.jsonify(**context), 200
