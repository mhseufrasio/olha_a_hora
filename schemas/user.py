from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dumpy_only=True)
    email = fields.Email(required=True)
