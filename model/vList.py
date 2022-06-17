import datetime

import snowflake.client
from sqlalchemy.orm import relationship

from comment.extends import db
from model.base import Base


class VList(db.Model, Base):
    __tablename__ = 'vlist'
    name = db.Column(db.String)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    like = db.Column(db.Integer)
    cover = db.Column(db.String)
    describe = db.Column(db.String)
    user = relationship("User")

    def __init__(self, title, uid, describe):
        now = datetime.datetime.now()
        self.id = snowflake.client.get_guid()
        self.title = title
        self.uid = uid
        self.like = 0
        self.describe = describe
        self.create_time = now
        self.update_time = now
        self.state = 1
