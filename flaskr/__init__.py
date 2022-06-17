from configparser import ConfigParser

from flask import Flask
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from blueprints import video, product, star, tag, user, follow, comment, vList, record
from comment.extends import db, cache, redis_client, mgo_db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    # 配置
    cfg = ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    db_host, db_port = cfg.get('db', 'host'), cfg.get('db', 'port')
    db_user, db_password, db_name = cfg.get('db', 'user'), cfg.get('db', 'password'), cfg.get('db', 'name')
    limit = cfg.get('server', 'limit')
    redis_host, redis_port = cfg.get('redis', 'host') or None, cfg.get('redis', 'port') or None
    redis_user, redis_password = cfg.get('redis', 'user') or None, cfg.get('redis', 'password') or None
    register = cfg.getboolean('server', 'register')
    mgo_config = {
        'db': cfg.get('mongo', 'db'),
        'host': cfg.get('mongo', 'host'),
        'port': cfg.getint('mongo', 'port'),
        'username': cfg.get('mongo', 'username'),
        'password': cfg.get('mongo', 'password')
    }

    # json 不排序
    app.config['JSON_SORT_KEYS'] = False

    # json 中文
    app.config['JSON_AS_ASCII'] = False

    # 数据库连接
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # JWT KEY
    app.config['SECRET_KEY'] = "\xc0\x00v\xc4\x9fe\x18\xb6\x8a^\x97C\x8e<\xc2\xdb7\xad\xe3\xf6\xf5\x98\x0c3"

    # register switch
    app.config['register'] = register

    class APSchedulerJobConfig(object):
        SCHEDULER_API_ENABLED = True
        JOBS = [
            {
                'id': '1',
                'func': 'scheduler.redis:update_product_follow',
                'args': '',
                'trigger': 'cron',
                'day': '*',
                'hour': '0',
                'minute': '0',
                'second': '0',
            },
            {
                'id': '2',
                'func': 'scheduler.redis:update_video_comments',
                'args': '',
                'trigger': 'cron',
                'day': '*',
                'hour': '12',
                'minute': '0',
                'second': '0',
            }
        ]

    # scheduler
    app.config.from_object(APSchedulerJobConfig())

    # redis 连接
    if redis_password is not None:
        redis_url = "redis://:%s@%s:%s/%s" % (redis_password, redis_host, redis_port, db_name)
    else:
        redis_url = "redis://@%s:%s/%s" % (redis_host, redis_port, db_name)
    app.config['REDIS_URL'] = redis_url

    # 限速
    Limiter(app=app, key_func=get_remote_address, default_limits=[limit])

    # init
    app.config['MONGODB_SETTINGS'] = mgo_config

    db.init_app(app)
    cache.init_app(app)
    # todo connection pool
    redis_client.init_app(app, encoding='utf8', decode_responses=True)
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    mgo_db.init_app(app)

    app.register_blueprint(video.vd)
    app.register_blueprint(product.pd)
    app.register_blueprint(star.sr)
    app.register_blueprint(tag.tg)
    app.register_blueprint(user.ur)
    app.register_blueprint(follow.fl)
    app.register_blueprint(comment.cm)
    app.register_blueprint(vList.vl)
    app.register_blueprint(record.rd)
    return app
