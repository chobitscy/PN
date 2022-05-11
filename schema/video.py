from marshmallow import fields

from schema.base import BaseSchema
from schema.product import ProductSchema


class VideoSchema(BaseSchema):
    vid = fields.String()
    title = fields.String()
    create_date = fields.DateTime()
    info_hash = fields.String()
    size = fields.Float()
    speeders = fields.String()
    downloads = fields.String()
    completed = fields.String()
    rate = fields.Float()
    screenshot = fields.String()
    pub_date = fields.DateTime()
    thumb = fields.String()
    print_screen = fields.String()
    tid = fields.String()
    pid = fields.Integer()
    product = fields.Nested(ProductSchema, only=('id', 'name', 'home', 'avatar'))
    comments = fields.Integer()
