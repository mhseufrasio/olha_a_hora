from db import db


class PosologiaModel(db.Model):
    __tablename__ = "posologias"

    id = db.Column(db.Integer, primary_key=True)
    dias_qtd = db.Column(db.Integer, nullable=False)
    frequencia = db.Column(db.Integer, nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey("medicamentos.id"), nullable=False)
    id_via = db.Column(db.Integer, db.ForeignKey("vias.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)