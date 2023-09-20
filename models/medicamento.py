from db import db


class MedicamentoModel(db.Model):
    __tablename__ = "medicamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)