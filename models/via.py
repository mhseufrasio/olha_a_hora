from db import db


class ViaModel(db.Model):
    __tablename__ = "vias"

    id = db.Column(db.Integer, primary_key=True)
    tipo_via = db.Column(db.String(80), unique=True, nullable=False)

    posologias = db.relationship("PosologiaModel", back_populates="via", lazy="dynamic")