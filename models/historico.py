from db import db
from datetime import datetime


class HistoricoModel(db.Model):
    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    confirmacao = db.Column(db.Boolean, nullable=False)
    id_horario = db.Column(db.Integer, db.ForeignKey("horarios.id"), unique=True, nullable=False)

    horario = db.relationship("HorarioModel", back_populates="historico")