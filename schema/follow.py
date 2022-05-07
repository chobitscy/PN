from marshmallow import fields

from schema.base import BaseSchema
from schema.product import ProductSchema


class FollowSchema(BaseSchema):
    pid = fields.Integer()
    uid = fields.Integer()
    Product = fields.Nested(ProductSchema)
