from marshmallow_mongoengine import ModelSchema, fields

from model.comment import Comment


class CommentSchema(ModelSchema):
    uid = fields.Integer()
    username = fields.String()
    vid = fields.Integer()
    content = fields.String()
    create_time = fields.DateTime()

    class Meta:
        model = Comment
