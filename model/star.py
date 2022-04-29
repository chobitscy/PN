from comment.extends import db
from model.base import Base


class Star(db.Model, Base):
    __tablename__ = 'star'
    vid = db.Column(db.BigInteger)
    pid = db.Column(db.BigInteger)
    aid = db.Column(db.BigInteger)
    uid = db.Column(db.BigInteger)
