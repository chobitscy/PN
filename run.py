import datetime
import hashlib
import json
import logging
import sys
import time

import flask_limiter
from flask import Flask, jsonify, abort, make_response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)

# json 不排序
app.config['JSON_SORT_KEYS'] = False

# json 中文
app.config['JSON_AS_ASCII'] = False

# 数据库连接
args = sys.argv
if len(args) <= 1:
    raise ValueError('参数不完整')
db_host, db_port, db_user, db_password, db_name, host, env = args[1], args[2], args[3], args[4], args[5], args[6], args[
    7]
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)
db = SQLAlchemy(app)

# 限速
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["2/minute"])


class BaseMixin:
    id = db.Column(db.BigInteger, primary_key=True)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    state = db.Column(db.Integer)


class Video(db.Model, BaseMixin):
    __tablename__ = 'video'
    vid = db.Column(db.String)
    title = db.Column(db.String)
    create_date = db.Column(db.DateTime)
    info_hash = db.Column(db.String)
    size = db.Column(db.Float)
    speeders = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    rate = db.Column(db.Float)
    screenshot = db.Column(db.String)
    pub_date = db.Column(db.DateTime)


class BaseSchema(Schema):
    id = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    state = fields.Integer()


class VideoSchema(BaseSchema):
    vid = fields.String()
    title = fields.String()
    create_date = fields.DateTime()
    info_hash = fields.String()
    size = fields.Float()
    speeders = fields.String()
    downloads = fields.String()
    completed = fields.String()
    rate = fields.Float()
    screenshot = fields.String()
    pub_date = fields.DateTime()


# 全局异常处理
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, flask_limiter.errors.RateLimitExceeded):
        return jsonify({
            'message': 'Too Many Requests'
        }), 429
    logging.exception(e)
    return jsonify({
        'message': 'system error'
    }), 500


# 请求拦截
@app.before_request
def request_handle():
    timestamp = request.headers.get('timestamp', 0, int)
    sign = request.headers.get('sign', None, str)
    if timestamp == 0 or sign is None:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))
    # 当客户端和服务器的时间相差 20 秒，客户端错误
    if env != 'dev' and int(round(time.time() * 1000)) - int(timestamp) > 20 * 1000:
        abort(make_response(jsonify({'message': 'timeout'}), 400))
    value = str(hashlib.md5(str('%.2f' % float(timestamp / len(request.path))).encode('utf-8')).hexdigest()).upper()
    if value is None or value != sign:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))


@app.route('/popular/<day>', methods=['GET'])
def get_list(day):
    page, pages, sort = parameter_handler(Video, '-rate')
    try:
        day = int(day)
    except ValueError:
        error('parameter error', 400)
    now = datetime.datetime.now()
    pagination = Video.query \
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now)) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return jsonify({
        'data': {
            'record': json.loads(VideoSchema().dumps(pagination.items, many=True)),
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total
        }
    })


def error(message, code):
    abort(make_response(jsonify({'message': message}), code))


def parameter_handler(o: db.Model, default_sort):
    page = request.args.get('page', 1, int)
    pages = request.args.get('pages', 10, int)
    sort = request.args.get('sort_by', default_sort, str)
    sort_way = sort[0]
    sort_by = sort[1:]
    attribute = None
    if hasattr(o, sort_by):
        attribute = getattr(o, sort_by)
        if sort_way == '-':
            attribute = attribute.desc()
    else:
        error('parameter error', 400)
    return page, pages, attribute


if __name__ == '__main__':
    app.run(host=host)
