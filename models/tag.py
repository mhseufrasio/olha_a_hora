from db import db


class EtiquetaModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(255), unique=True, nullable=False)
    hex = db.Column(db.String(255), unique=True, nullable=False)

    schedule = db.relationship("ScheduleModel", back_populates="tags", lazy="dynamic")