from marshmallow import fields

from schema.base import BaseSchema
from schema.user import UserSchema


class VListSchema(BaseSchema):
    title = fields.String()
    uid = fields.Integer()
    like = fields.Integer()
    cover = fields.String()
    describe = fields.String()
    user = fields.Nested(UserSchema(), only={"name", "avatar", "email"})