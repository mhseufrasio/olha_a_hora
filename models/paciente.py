from db import db


class PacienteModel(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    observation = db.Column(db.String(255), nullable=True)
    chave_acompanhante = db.Column(db.String(40), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    usuario = db.relationship("UsuarioModel", back_populates="pacientes")

    posologias = db.relationship("PosologiaModel", back_populates="pacientes", lazy="dynamic")
