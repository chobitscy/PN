from marshmallow import fields

from schema.base import BaseSchema


class StarSchema(BaseSchema):
    vid = fields.Integer()
    pid = fields.Integer()
    aid = fields.Integer()
    uid = fields.Integer()
