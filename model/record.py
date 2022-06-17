import datetime

import snowflake.client
from sqlalchemy.orm import relationship

from comment.extends import db
from model.base import Base


class Record(db.Model, Base):
    __tablename__ = 'record'
    vlist_id = db.Column(db.Integer)
    vid = db.Column(db.Integer)
    video = relationship("Video")

    def __init__(self, vlist_id, vid):
        now = datetime.datetime.now()
        self.id = snowflake.client.get_guid()
        self.vlist_id = vlist_id
        self.vid = vid
        self.create_time = now
        self.update_time = now
        self.state = 1