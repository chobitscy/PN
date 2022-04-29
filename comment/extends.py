from flask_sqlalchemy import SQLAlchemy

from configparser import ConfigParser

from flask_caching import Cache
from redis import Redis

cfg = ConfigParser()
cfg.read('config.ini', encoding='utf-8')
expired, env = cfg.getint('server', 'expired') or None, cfg.get('server', 'env') or None
redis_host, redis_port = cfg.get('redis', 'host') or None, cfg.get('redis', 'port') or None
redis_user, redis_password = cfg.get('redis', 'user') or None, cfg.get('redis', 'password') or None

Redis()
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

db = SQLAlchemy()
