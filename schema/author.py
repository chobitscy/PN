from marshmallow import fields

from schema.base import BaseSchema


class AuthorSchema(BaseSchema):
    name = fields.String()
    home = fields.String()
    avatar = fields.String()
