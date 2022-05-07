import functools

from flask import request

from model.user import User


def auth(func):
    @functools.wraps(func)
    def wrapper():
        token = request.headers["Authorization"]
        return func(User.decode_auth_token(token))

    return wrapper
