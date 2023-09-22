from marshmallow import Schema, fields
from schemas.usuario import PlainUsuarioSchema


class PlainPacienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    data_nascimento = fields.DateTime(required=True, format="%d%m%Y")
    observacao = fields.Str(required=True)


class PacienteSchema(PlainPacienteSchema):
    id_usuario = fields.Int(load_only=True, required=True)

    usuario = fields.Nested(PlainUsuarioSchema(), dumpy_only=True)