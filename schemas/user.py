from marshmallow import Schema, fields
from schemas.paciente import PlainPatientSchema


class PlainUserSchema(Schema):
    id = fields.Int(dumpy_only=True)
    email = fields.Email(required=True)


class UserSchema(PlainUserSchema):
    patients = fields.List(fields.Nested(PlainPatientSchema(), dumpy_only=True))
