""" Aplicação em Flask Para o Controle de Horários de Tomada de Remédios"""
import os
import pathlib

import requests

from flask import Flask, render_template, request, url_for, redirect, session, abort
from flask_smorest import Api
from dotenv import load_dotenv
from pip._vendor import cachecontrol
from db import db
from models import PacienteModel, UsuarioModel
from flask_migrate import Migrate


def create_app(db_url=None):
    """Configurações da Aplicação e Rotas de Acesso"""
    app = Flask(__name__, template_folder="templates")
    load_dotenv()
    app.config["SECRET_KEY"] = "SECRet"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Olha A Hora"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)
    Migrate(app=app, db=db, compare_type=True)

    """    def login_is_required(function):
            if "user_id" not in session:
                return render_template('login.html')
            return function()"""

    @app.route("/", endpoint="index")
    def index():
        return render_template('login.html')

    @app.route("/home", endpoint="home")
    # @login_is_required
    def home():
        all_patients = PacienteModel.query.all()
        return render_template('index.html', patients=all_patients)

    @app.route("/login", methods=["POST"], endpoint="login")
    def login():
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        usuario = UsuarioModel.query.filter_by(cpf=cpf).first()
        if usuario and usuario.senha == senha:
            return redirect(url_for('home'))
        return render_template('login.html')

    @app.route("/logout", endpoint="logout")
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route("/register", methods=["GET", "POST"], endpoint="register")
    def register():
        if request.method == "POST":
            user = UsuarioModel()
            user.cpf = request.form['cpf']
            user.senha = request.form['senha']
            usuario = UsuarioModel.query.filter_by(cpf=user.cpf).first()
            if not usuario:
                db.session.add(user)
                db.session.commit()
                return render_template('login.html')
        return render_template('register.html')

    @app.route("/add_patient", methods=["POST"], endpoint="add_patient")
    # @login_is_required
    def add_patient():
        patient = PacienteModel()
        patient.name = request.form['name']
        patient.birth_date = request.form['birth_date']
        patient.observation = request.form['observation']
        patient.user_id = request.form['user_id']
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('home'))

    @app.route("/update", methods=["POST"], endpoint="update_patient")
    # @login_is_required
    def update_patient():
        patient = PacienteModel.query.get(request.form['id'])
        patient.name = request.form['name_edit']
        patient.birth_date = request.form['birth_date_edit']
        patient.observation = request.form['observation_edit']
        db.session.commit()
        return redirect(url_for('home'))

    @app.route("/delete/<id>", endpoint="delete_by_id")
    def delete_by_id(id_patient):
        patient = PacienteModel.query.get_or_404(id_patient)
        db.session.delete(patient)
        db.session.commit()
        return redirect(url_for('home'))

    if __name__ == "__main__":
        app.run()

    return app
