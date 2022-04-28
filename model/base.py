from comment.db import db


class Base:
    id = db.Column(db.BigInteger, primary_key=True)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    state = db.Column(db.Integer)
