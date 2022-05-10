from comment.extends import db
from model.base import Base


class Product(db.Model, Base):
    __tablename__ = 'product'
    name = db.Column(db.String)
    home = db.Column(db.String)
    avatar = db.Column(db.String)
    works = db.Column(db.Integer)
    fans = db.Column(db.Integer)
    follow = db.Column(db.Integer)
