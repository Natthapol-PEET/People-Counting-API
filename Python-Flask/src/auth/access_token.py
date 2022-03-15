from flask import abort
from configs import config


def authentication(headers):
    token = None

    if 'x-access-tokens' in headers:
        token = headers['x-access-tokens']

    if token not in config.X_ACCRESS_TOKENS:
        abort(401)
