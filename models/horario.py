from db import db


class HorarioModel(db.Model):
    __tablename__ = "horarios"
    # atributos
    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.TIME(), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey("tags.id"), unique=False, nullable=False)
    id_posologia = db.Column(db.Integer, db.ForeignKey("posologias.id"), unique=False, nullable=False)

    # relações muitos para 1
    tag = db.relationship("EtiquetaModel", back_populates="horario")
    posologias = db.relationship("PosologiaModel", back_populates="horario")

    # relações 1 para muitos
    historico = db.relationship("HistoricoModel", back_populates="horario", lazy="dynamic")
