from marshmallow import fields

from schema.base import BaseSchema


class UserSchema(BaseSchema):
    name = fields.String()
    avatar = fields.String()
    email = fields.String()
