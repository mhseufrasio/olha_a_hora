from db import db


class HorarioModel(db.Model):
    __tablename__ = "horarios"

    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.TIME(), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey("etiquetas.id"), unique=False, nullable=False)
    id_posologia = db.Column(db.Integer, db.ForeignKey("posologias.id"), unique=False, nullable=False)