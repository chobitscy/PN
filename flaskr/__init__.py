from configparser import ConfigParser

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from blueprints import video, product, star, tag, user, follow
from comment.extends import db, cache


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    # json 不排序
    app.config['JSON_SORT_KEYS'] = False
    # json 中文
    app.config['JSON_AS_ASCII'] = False
    # 配置
    cfg = ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    db_host, db_port = cfg.get('db', 'host'), cfg.get('db', 'port')
    db_user, db_password, db_name = cfg.get('db', 'user'), cfg.get('db', 'password'), cfg.get('db', 'name')
    limit = cfg.get('server', 'limit')
    # 数据库连接
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = "\xc0\x00v\xc4\x9fe\x18\xb6\x8a^\x97C\x8e<\xc2\xdb7\xad\xe3\xf6\xf5\x98\x0c3"

    # 限速
    Limiter(app=app, key_func=get_remote_address, default_limits=[limit])

    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(video.vd)
    app.register_blueprint(product.pd)
    app.register_blueprint(star.sr)
    app.register_blueprint(tag.tg)
    app.register_blueprint(user.ur)
    app.register_blueprint(follow.fl)
    return app
