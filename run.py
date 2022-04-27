import datetime
import hashlib
import json
import logging
import time
from configparser import ConfigParser
from enum import Enum

import flask_limiter
from flask import Flask, jsonify, abort, make_response, request
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from redis import Redis

app = Flask(__name__)

# json 不排序
app.config['JSON_SORT_KEYS'] = False

# json 中文
app.config['JSON_AS_ASCII'] = False

# 配置
cfg = ConfigParser()
cfg.read('config.ini', encoding='utf-8')
db_host, db_port = cfg.get('db', 'host'), cfg.get('db', 'port')
db_user, db_password, db_name = cfg.get('db', 'user'), cfg.get('db', 'password'), cfg.get('db', 'name')
host, limit = cfg.get('server', 'host'), cfg.get('server', 'limit')
expired, env = cfg.getint('server', 'expired'), cfg.get('server', 'env')
redis_host, redis_port = cfg.get('redis', 'host'), cfg.get('redis', 'port')
redis_user, redis_password = cfg.get('redis', 'user'), cfg.get('redis', 'password')

# 数据库连接
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 限速
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=[limit])

redis = Redis()
if redis_user is None or redis_password is None:
    redis_url = 'redis://%s:%s' % (redis_host, redis_port)
else:
    redis_url = 'redis://%s:%s@%s:%s' % (redis_user, redis_password, redis_host, redis_port)
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'PN',
    'CACHE_DEFAULT_TIMEOUT': 60 * expired,
    'CACHE_REDIS_URL': redis_url
})
cache.init_app(app)


class BaseMixin:
    id = db.Column(db.BigInteger, primary_key=True)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    type_id = db.Column(db.Integer)


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
    thumb = db.Column(db.String)
    print_screen = db.Column(db.String)
    author = db.Column(db.String)
    author_home = db.Column(db.String)
    tags = db.Column(db.String)
    product = db.Column(db.String)


class BaseSchema(Schema):
    id = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    state = fields.Integer()
    type_id = fields.Integer()


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
    thumb = fields.String()
    print_screen = fields.String()
    author = fields.String()
    author_home = fields.String()
    tags = fields.String()
    product = fields.String()


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
    if env == 'dev':
        return
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


# 流行
@app.route('/popular/<type_id>/<day>', methods=['GET'])
@cache.cached(query_string=True)
def popular(type_id, day):
    page, pages, sort = parameter_handler(Video, '-rate')
    try:
        day = int(day)
        type_id = int(type_id)
    except ValueError:
        error('parameter error', 400)
    now = datetime.datetime.now()
    pagination = Video.query \
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now),
                Video.type_id == type_id) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


# 搜索
@app.route('/search/<vid>', methods=['GET'])
@cache.cached(query_string=True)
def vid_search(vid: str):
    return search(Video, 'vid', vid, condition_way.LIKE.value)


# 产品
@app.route('/product/<product>', methods=['GET'])
@cache.cached(query_string=True)
def product_search(product: str):
    return search(Video, 'product', product, condition_way.EQUAL.value)


# 作者
@app.route('/author/<author>', methods=['GET'])
@cache.cached(query_string=True)
def author_search(author: str):
    return search(Video, 'author', author, condition_way.EQUAL.value)


class condition_way(Enum):
    LIKE = 1
    EQUAL = 2


def search(model: object, attribute: str, target: str, way: int):
    if hasattr(model, attribute) is False:
        raise ValueError('attribute error')
    condition = None
    if way == condition_way.LIKE.value:
        condition = getattr(model, attribute).like('%' + target + '%')
    elif way == condition_way.EQUAL.value:
        condition = getattr(model, attribute) == target
    if condition is None:
        raise ValueError('condition error')
    page, pages, sort = parameter_handler(Video, '-rate')
    pagination = model.query \
        .filter(condition) \
        .order_by(sort) \
        .paginate(page, per_page=pages, error_out=False)
    return pagination_result(VideoSchema(), pagination)


def pagination_result(o: BaseSchema, pagination):
    return jsonify({
        'data': {
            'record': json.loads(o.dumps(pagination.items, many=True)),
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
