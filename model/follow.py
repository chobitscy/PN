import datetime

import snowflake.client

from comment.extends import db
from model.base import Base
from model.product import Product
from utils.response import error


class Follow(db.Model, Base):
    __tablename__ = 'follow'
    pid = db.Column(db.String, db.ForeignKey('product.id'))
    uid = db.Column(db.BigInteger)

    def __init__(self, pid, uid):
        if Product.query.filter(Product.id == pid).first() is None:
            error('vid is not find', 500)
        if Follow.query.filter(Follow.pid == pid, Follow.uid == uid, Follow.state == 1).first() is not None:
            error('already Followed', 500)
        now = datetime.datetime.now()
        self.pid = pid
        self.uid = uid
        self.id = snowflake.client.get_guid()
        self.create_time = now
        self.update_time = now
        self.state = 1
