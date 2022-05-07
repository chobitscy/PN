import datetime

import snowflake.client
from sqlalchemy.orm import relationship

from comment.extends import db
from model.base import Base
from model.video import Video
from utils.response import error


class Star(db.Model, Base):
    __tablename__ = 'star'
    vid = db.Column(db.BigInteger, db.ForeignKey('video.vid'))
    uid = db.Column(db.BigInteger)
    video = relationship("Video")

    def __init__(self, vid, uid):
        if Video.query.filter(Video.vid == vid).first() is None:
            error('vid is not find', 500)
        if Star.query.filter(Star.vid == vid, Star.uid == uid, Star.state == 1).first() is not None:
            error('already stared', 500)
        now = datetime.datetime.now()
        self.vid = vid
        self.uid = uid
        self.id = snowflake.client.get_guid()
        self.create_time = now
        self.update_time = now
        self.state = 1
