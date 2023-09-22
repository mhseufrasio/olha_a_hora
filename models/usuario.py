from db import db


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    pacientes = db.relationship("PacienteModel", back_populates="usuario", lazy="dynamic")
    posologias = db.relationship("PosologiaModel", back_populates="usuario", lazy="dynamic")
