from marshmallow import fields

from schema.base import BaseSchema


class ProductSchema(BaseSchema):
    name = fields.String()
    home = fields.String()
