from marshmallow import fields

from schema.base import BaseSchema


class UserSchema(BaseSchema):
    email = fields.String()
