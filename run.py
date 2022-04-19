import datetime
import hashlib
import json
import logging
import sys
import time

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
db_host, db_port, db_user, db_password, db_name, host = args[1], args[2], args[3], args[4], args[5], args[6]
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)
db = SQLAlchemy(app)

# 限速
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["20/minute"])


class BaseMixin:
    id = db.Column(db.BigInteger, primary_key=True)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    state = db.Column(db.Integer)


class Video(db.Model, BaseMixin):
    __tablename__ = 'video'
    vid = db.Column(db.String)
    rate = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)


class BaseSchema(Schema):
    id = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    state = fields.Integer()


class VideoSchema(BaseSchema):
    vid = fields.String()
    rate = fields.Float()
    pub_date = fields.DateTime()


# 全局异常处理
@app.errorhandler(Exception)
def handle_exception(e):
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
    if int(round(time.time() * 1000)) - int(timestamp) > 20 * 1000:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))
    value = str(hashlib.md5(str('%.2f' % float(timestamp / len(request.url))).encode('utf-8')).hexdigest()).upper()
    if value is None or value != sign:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))


@app.route('/popular/<day>', methods=['GET'])
def get_list(day):
    page = request.args.get('page', 1, int)
    pages = request.args.get('pages', 10, int)
    try:
        day = int(day)
    except ValueError:
        abort(make_response(jsonify({'message': 'parameter error'}), 400))
    now = datetime.datetime.now()
    pagination = Video.query \
        .filter(Video.pub_date.between(now - datetime.timedelta(days=day), now)) \
        .order_by(Video.rate.desc()) \
        .paginate(page, per_page=pages, error_out=False)
    return jsonify({
        'data': {
            'record': json.loads(VideoSchema().dumps(pagination.items, many=True)),
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total
        }
    })


if __name__ == '__main__':
    app.run(host=host)
