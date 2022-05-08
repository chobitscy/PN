import decimal
import hashlib
import logging
import time
from configparser import ConfigParser

import flask_limiter
from flask import jsonify, request, abort, make_response

from flaskr import create_app
from model.user import User
from utils.response import error

app = create_app()

dev = 'dev'


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
    if env == dev:
        return
    timestamp = request.headers.get('timestamp', 0, int)
    sign = request.headers.get('sign', None, str)
    path = request.path
    if timestamp == 0 or sign is None:
        abort(make_response(jsonify({'message': 'illegal request'}), 400))
    # 当客户端和服务器的时间相差 20 秒，客户端错误
    if env != 'dev' and int(round(time.time() * 1000)) - int(timestamp) > 20 * 1000:
        abort(make_response(jsonify({'message': 'timeout'}), 400))
    decimal.getcontext().rounding = "ROUND_HALF_UP"
    res = decimal.Decimal(str(float(timestamp / len(path)))).quantize(decimal.Decimal("0.00"))
    value = str(
        hashlib.md5(str(res).encode('utf-8')).hexdigest()).upper()
    if value is None or value != sign:
        abort(make_response(jsonify({'message': 'sign error'}), 400))
    # register or login not auth
    if path == '/user/register' or path == '/user/login':
        return
    if 'Authorization' not in request.headers:
        error('auth error', 401)
    token = request.headers["Authorization"]
    User.decode_auth_token(token)


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    env = cfg.get('server', 'env')
    host = cfg.get('server', 'host')
    app.run(host=host)
