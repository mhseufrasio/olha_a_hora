from datetime import datetime

from db import db


class HorarioModel(db.Model):
    __tablename__ = "horarios"
    # atributos
    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.TIME(), nullable=False)
    id_posologia = db.Column(db.Integer, db.ForeignKey("posologias.id"), unique=False, nullable=False)
    tomou = db.Column(db.Boolean, unique=False, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow())

    # relações muitos para 1
    posologias = db.relationship("PosologiaModel", back_populates="horario")
