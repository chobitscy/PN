import hashlib
import re

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from comment.extends import db
from model.user import User
from schema.user import UserSchema
from utils.response import error

ur = Blueprint('user', __name__, url_prefix='/user')


@ur.route('/register', methods=['POST'])
def register():
    email = request.form.get('email') or None
    password = request.form.get('password') or None
    if email is None or password is None:
        error('email or password is null', 400)
    regEx = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(regEx, email) is None:
        error('email format error', 400)
    user = User(email, password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        error('email repeat', 400)
    token = user.encode_auth_token(user.id)
    return jsonify({
        'data': {
            'user': UserSchema(only=('id', 'email')).dump(user),
            'token': str(token)
        }
    })


@ur.route('/login', methods=['POST'])
def login():
    email = request.form.get('email') or None
    password = request.form.get('password') or None
    expired = int(request.form.get('expired', 1))
    if email is None or password is None:
        error('email or password is null', 400)
    password = hashlib.md5(password.encode('utf8')).hexdigest()
    res = User.query.filter(User.email == email, User.password == password).first()
    if res is None:
        error('auth failure', 400)
    return jsonify({
        'data': {
            'user': UserSchema(only=('id', 'email')).dump(res),
            'token': str(User.encode_auth_token(res.id, expired=expired))
        }
    })
