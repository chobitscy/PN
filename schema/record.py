from marshmallow import fields

from schema.base import BaseSchema
from schema.video import VideoSchema


class RecordSchema(BaseSchema):
    vlist_id = fields.Integer()
    vid = fields.Integer()
    video = fields.Nested(VideoSchema())
