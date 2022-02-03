"""Get post details."""
import insta485


def get_post_info(username, postid_url_slug):
    """Get post details infomation."""
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT filename as img_url, owner, created "
        "FROM posts "
        "WHERE postid = ?", (postid_url_slug,))
    info = cur.fetchall()[0]

    # Get whether the user like the post
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? and postid = ?", (username, postid_url_slug,))
    like_ = cur.fetchall()
    like_url = None
    if len(like_) == 1:
        like_url = "/api/v1/likes/" + str(like_[0]['likeid']) + "/"

    # Get the number of likes of the specific post
    cur = connection.execute(
        "SELECT count(likeid) as numlikes "
        "FROM likes "
        "WHERE postid = ?", (postid_url_slug,))
    # numlikes = cur.fetchall()[0]['numlikes']

    likes = {
        "lognameLikesThis": (1 if len(like_) == 1 else 0),
        # "numLikes": numlikes,
        "numLikes": cur.fetchall()[0]['numlikes'],
        "url": like_url,
    }

    # Get the comment list of the post
    commentid_list = []
    cur = connection.execute(
        "SELECT commentid "
        "FROM comments "
        "WHERE postid = ? "
        "ORDER BY commentid asc", (postid_url_slug,))
    # list_ = cur.fetchall()
    # for c_id in list_:
    for c_id in cur.fetchall():
        commentid_list.append(c_id['commentid'])

    comments = []
    for cid in commentid_list:
        cur = connection.execute(
            "SELECT commentid, owner, text "
            "FROM comments "
            "WHERE commentid = ?", (cid,))
        comment_info = cur.fetchall()[0]
        comment = {
            "commentid": comment_info['commentid'],
            "lognameOwnsThis": username == comment_info['owner'],
            "owner": comment_info['owner'],
            "ownerShowUrl": "/users/" + comment_info['owner'] + "/",
            "text": comment_info['text'],
            "url": "/api/v1/comments/" + str(comment_info['commentid']) + "/",
        }
        comments.append(comment)

    cur = connection.execute(
        "SELECT filename FROM users WHERE username = ?", (info['owner'],)
    )
    # filename = cur.fetchall()[0]['filename']

    context = {
        "comments": comments,
        "created": info['created'],
        "imgUrl": "/uploads/" + info['img_url'],
        "likes": likes,
        "owner": info['owner'],
        # "ownerImgUrl": '/uploads/' + filename,
        "ownerImgUrl": '/uploads/' + cur.fetchall()[0]['filename'],
        "ownerShowUrl": "/users/" + info['owner'] + "/",
        "postShowUrl": "/posts/" + str(postid_url_slug) + "/",
        "postid": postid_url_slug,
        # "url": flask.request.path,
    }

    return context
