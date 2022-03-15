from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

basic_auth = HTTPBasicAuth()

users = {
    "user": generate_password_hash("passwd"),
    "admin": generate_password_hash("public"),
}


@basic_auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@basic_auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
