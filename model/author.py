from comment.extends import db
from model.base import Base


class Author(db.Model, Base):
    __tablename__ = 'author'
    name = db.Column(db.String)
    home = db.Column(db.String)
    avatar = db.Column(db.String)