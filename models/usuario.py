from db import db


class UserModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    celular = db.Column(db.String(20))

    pacientes = db.relationship("PacienteModel", back_populates="usuario", lazy="dynamic")
    posologias = db.relationship("PosologiaModel", back_populates="usuario", lazy="dynamic")
