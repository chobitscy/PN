import hashlib
import re

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from comment.extends import db
from model.comment import Comment
from model.user import User
from schema.user import UserSchema
from template.result import operation_response
from utils.response import error, get_from
from wrapper.auth import auth

ur = Blueprint('user', __name__, url_prefix='/user')


def exist(name: str) -> bool:
    return db.session.query(exists().where(User.name == name)).scalar()


@ur.route('/register', methods=['POST'])
def register():
    if current_app.config['register'] is False:
        error('Not allowed register', 403)
    name = request.form.get('name', default=None, type=str)
    email = request.form.get('email', default=None, type=str)
    password = request.form.get('password', default=None, type=str)
    if name is None or email is None or password is None:
        error('name or email or password is null', 400)
    regEx = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(regEx, email) is None:
        error('email format error', 400)
    if exist(name):
        error('user already exist', 500)
    user = User(name, email, password)
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
        error('auth failure', 401)
    return jsonify({
        'data': {
            'user': UserSchema(only=('id', 'email')).dump(res),
            'token': str(User.encode_auth_token(res.id, expired=expired)),
            'ip': request.headers['X-Real-IP']
        }
    })


@ur.route('/update', methods=["POST"])
@auth
def _update(uid):
    _id = get_from('id', int)
    name = get_from('name', str)
    email = get_from('email', str)
    avatar = get_from('avatar', str)
    if _id != uid:
        error('Only the current user can modify it', 403)
    User.query.filter(User.id == _id).update({'name': name, 'email': email, 'avatar': avatar})
    db.session.commit()
    # update comment username
    comment = Comment.objects(uid=uid, username_ne=name)
    comment.username = name
    comment.update()
    return operation_response(True)
