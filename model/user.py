import datetime
import hashlib
import uuid

import jwt
import snowflake.client
from flask import current_app, request

from comment.extends import db
from model.base import Base
from utils.response import error


class User(db.Model, Base):
    __tablename__ = 'user'
    email = db.Column(db.String)
    password = db.Column(db.String)
    ip = db.Column(db.String)

    def __init__(self, email, password):
        self.id = snowflake.client.get_guid()
        self.email = email
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()
        self.ip = request.remote_addr
        now = datetime.datetime.now()
        self.create_time = now
        self.update_time = now
        self.state = 1

    @staticmethod
    def encode_auth_token(user_id, expired=1):
        """
        Generates the Auth Token
        :param user_id 用户 id
        :param expired 过期时间（单位：天）
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expired),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            error('Signature expired. Please log in again', 401)
        except jwt.InvalidTokenError:
            error('Invalid token. Please log in again', 401)
