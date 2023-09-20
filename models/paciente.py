from db import db


class PacienteModel(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.String(256), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    usuario = db.relationship("UsuarioModel", back_populates="pacientes")