from itertools import groupby

from comment.extends import redis_client, db
from flaskr import create_app
from model.product import Product
from model.video import Video


def update_product_follow():
    """
    每天 0 点更新相应 product 的 follow 数
    :return:
    """
    delay_update('delay_follow', Product, 'follow')


def update_video_comments():
    """
    每天 12 点更新 video 的 comment 数
    :return:
    """
    delay_update('delay_comments', Video, 'reply')


def delay_update(key: str, model: db.Model, field: str):
    """
    延迟更新数据
    :param key: redis list key
    :param model: 实体
    :param field: 更新字段
    :return:
    """
    app = create_app()
    with app.app_context():
        if redis_client.exists(key) == 1:
            data = redis_client.lrange(key, 0, -1)
            for _id, item in groupby(sorted(data), key=lambda x: x):
                total = len(list(item))
                model.query.filter(model.id == _id).update({field: getattr(model, field) + total})
                db.session.commit()
            redis_client.delete(key)
