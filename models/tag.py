from db import db


class EtiquetaModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(255), unique=True, nullable=False)
    hex = db.Column(db.String(255), unique=True, nullable=False)

    horario = db.relationship("HorarioModel", back_populates="tag", lazy="dynamic")