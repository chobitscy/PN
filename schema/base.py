from marshmallow import Schema, fields


class BaseSchema(Schema):
    id = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    state = fields.Integer()
