from comment.db import db
from model.base import Base


class Tag(db.Model, Base):
    __tablename__ = 'tag'
    name = db.Column(db.String)
