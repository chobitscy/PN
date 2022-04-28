from comment.db import db
from model.base import Base


class Product(db.Model, Base):
    __tablename__ = 'product'
    name = db.Column(db.String)
    home = db.Column(db.String)
