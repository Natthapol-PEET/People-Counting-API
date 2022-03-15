from flask_httpauth import HTTPTokenAuth

auth_token = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "Hr+nDkzo9rj9mm7oPtErLa0Ge/FLnrYhEBh0ZPFq6mIsblUt6/o2bO4Qvzm19HdN991qggwbNVq7fiqy76FwOw==": "john",
    "secret-token-2": "susan"
}

@auth_token.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
