"""REST API for index."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=['GET'])
def get_index():
    """Return index."""
    context = {
      "comments": "/api/v1/comments/",
      "likes": "/api/v1/likes/",
      "posts": "/api/v1/posts/",
      "url": flask.request.path,
    }
    return flask.jsonify(**context)
