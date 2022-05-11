from comment.extends import mgo_db


class Comment(mgo_db.Document):
    uid = mgo_db.IntField()
    username = mgo_db.StringField()
    vid = mgo_db.IntField()
    content = mgo_db.StringField()
    create_time = mgo_db.DateTimeField()

    meta = {
        'ordering': ['-create_time']
    }