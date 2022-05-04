from comment.extends import db


class Base:
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    state = db.Column(db.Integer)
