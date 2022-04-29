from sqlalchemy.orm import relationship

from comment.extends import db
from model.base import Base


class Video(db.Model, Base):
    __tablename__ = 'video'
    vid = db.Column(db.String)
    title = db.Column(db.String)
    create_date = db.Column(db.DateTime)
    info_hash = db.Column(db.String)
    size = db.Column(db.Float)
    speeders = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    rate = db.Column(db.Float)
    screenshot = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    thumb = db.Column(db.String)
    print_screen = db.Column(db.String)
    aid = db.Column(db.BigInteger, db.ForeignKey('author.id'))
    tid = db.Column(db.TEXT)
    pid = db.Column(db.BigInteger, db.ForeignKey('product.id'))
    product = relationship("Product")
    author = relationship("Author")
