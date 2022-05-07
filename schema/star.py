from marshmallow import fields

from schema.base import BaseSchema
from schema.video import VideoSchema


class StarSchema(BaseSchema):
    vid = fields.Integer()
    uid = fields.Integer()
    video = fields.Nested(VideoSchema)
