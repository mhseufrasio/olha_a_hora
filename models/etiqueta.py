from db import db


class EtiquetaModel(db.Model):
    __tablename__ = "etiquetas"

    id = db.Column(db.Integer, primary_key=True)
    cor = db.Column(db.String(80), unique=True, nullable=False)
    codigo_hexadecimal = db.Column(db.String(80), unique=True, nullable=False)