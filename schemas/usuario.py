from marshmallow import Schema, fields
from schemas.paciente import PlainPacienteSchema


class PlainUsuarioSchema(Schema):
    id = fields.Int(dumpy_only=True)
    email = fields.Email(required=True)


class UsuarioSchema(PlainUsuarioSchema):
    pacientes = fields.List(fields.Nested(PlainPacienteSchema(), dumpy_only=True))
