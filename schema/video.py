from marshmallow import fields

from schema.base import BaseSchema


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
    author = fields.String()
    author_home = fields.String()
    tags = fields.String()
    product = fields.String()
