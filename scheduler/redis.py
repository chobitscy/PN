from itertools import groupby

from comment.extends import redis_client, db
from flaskr import create_app
from model.product import Product


def update_product_follow():
    app = create_app()
    with app.app_context():
        key = 'delay_follow'
        if redis_client.exists(key) == 1:
            follow_list = redis_client.lrange(key, 0, -1)
            for k, g in groupby(sorted(follow_list), key=lambda x: x):
                total = len(list(g))
                Product.query.filter(Product.id == k).update({'follow': Product.follow + total})
                db.session.commit()
            redis_client.delete(key)
