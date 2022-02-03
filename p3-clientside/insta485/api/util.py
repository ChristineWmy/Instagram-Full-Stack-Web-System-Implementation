"""Status checking."""
import hashlib
import insta485


def error_checking(status_code):
    """Check status."""
    if status_code == 400:
        message = "Bad Request"
    if status_code == 403:
        message = "Forbidden"
    if status_code == 404:
        message = "Not Found"
    if status_code == 409:
        message = "Conflict"
    context = {
        "message": message,
        "status_code": status_code,
    }
    return context


def wrong_password(username, password):
    """Check the password whether is valid."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE users.username = ?", (username,)
    )
    pas = cur.fetchall()

    salt_ = pas[0]['password'].split('$')[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt_ + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt_, password_hash])

    curr = connection.execute(
        "SELECT 1 "
        "FROM users "
        "WHERE users.username = ? AND users.password = ?",
        (username, password_db_string)
    )
    result = curr.fetchall()
    return len(result) == 0


def invalid_postid(postid):
    """Get the max postid."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT max(postid) as max_postid "
        "FROM posts")
    max_postid = cur.fetchall()[0]['max_postid']
    return max_postid < postid
