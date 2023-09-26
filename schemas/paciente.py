from marshmallow import Schema, fields
from schemas.user import PlainUserSchema


class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    birth_date = fields.DateTime(required=True, format="%d%m%Y")
    observacion = fields.Str(required=True)


class PacienteSchema(PlainPatientSchema):
    user_id = fields.Int(load_only=True, required=True)

    user = fields.Nested(PlainUserSchema(), dumpy_only=True)