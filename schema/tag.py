from marshmallow import fields

from schema.base import BaseSchema


class TagSchema(BaseSchema):
    name = fields.String()
