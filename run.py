import hashlib
import logging
import time
from configparser import ConfigParser

import flask_limiter
from flask import jsonify, request, abort, make_response

from flaskr import create_app

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
    if timestamp == 0 or sign is None:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))
    # 当客户端和服务器的时间相差 20 秒，客户端错误
    if env != 'dev' and int(round(time.time() * 1000)) - int(timestamp) > 20 * 1000:
        abort(make_response(jsonify({'message': 'timeout'}), 400))
    value = str(hashlib.md5(str('%.2f' % float(timestamp / len(request.path))).encode('utf-8')).hexdigest()).upper()
    if value is None or value != sign:
        abort(make_response(jsonify({'message': 'Illegal request'}), 400))


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    env = cfg.get('server', 'env')
    app.run()
