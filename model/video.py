from comment.db import db
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
    author = db.Column(db.BigInteger, db.ForeignKey('author.id'))
    author_home = db.Column(db.String)
    tags = db.Column(db.String)
    product = db.Column(db.BigInteger, db.ForeignKey('product.id'))
