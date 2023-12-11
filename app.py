""" Aplicação em Flask Para o Controle de Horários de Tomada de Remédios"""
import calendar
import os
import time

import pandas as pd

import requests

from secrets import token_hex
from datetime import datetime, date

from flask import Flask, render_template, request, url_for, redirect, session, abort
from flask_smorest import Api
from dotenv import load_dotenv
from pip._vendor import cachecontrol
from db import db
from models import PacienteModel, UsuarioModel, MedicamentoModel, PosologiaModel, HorarioModel
from flask_migrate import Migrate


def create_app(db_url=None):
    """Configurações da Aplicação e Rotas de Acesso"""
    app = Flask(__name__, template_folder="templates", static_folder="static")
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

    @app.route("/", endpoint="index")
    def index():
        session['user_id'] = None
        return render_template('login.html')

    @app.route("/home", endpoint="home")
    # @login_is_required
    def home():
        if session['user_id'] is not None:
            all_patients = PacienteModel.query.all()
            return render_template('index.html', patients=all_patients)
        return render_template('login.html')

    @app.route("/login", methods=["POST"], endpoint="login")
    def login():
        session.pop('user_id', None)
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        usuario = UsuarioModel.query.filter_by(cpf=cpf).first()
        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.id
            return redirect(url_for('home'))
        return render_template('login.html')

    @app.route("/login_acompanhante", methods=["GET", "POST"], endpoint="login_acompanhante")
    def login_acompanhante():
        if request.method == "POST":
            cpf_paciente = request.form["cpf_paciente"]
            codigo_acesso = request.form["codigo_acesso"]
            paciente = PacienteModel.query.filter_by(cpf=cpf_paciente).first()
            if paciente and paciente.chave_acompanhante == codigo_acesso:
                return ver_perfil(paciente.id)
        return render_template('login_acompanhante.html')

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
        patient.cpf = request.form['cpf']
        patient.chave_acompanhante = token_hex(12)
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

    def cadastrar_remedio(medicacao):
        medicamento = MedicamentoModel()
        medicamento.nome = medicacao
        db.session.add(medicamento)
        db.session.commit()

    @app.route("/cadastrar_posologia", methods=["POST"], endpoint="cadastrar_posologia")
    def cadastrar_posologia():
        posologia = PosologiaModel()
        posologia.frequencia = request.form['frequencia']
        posologia.duracao = request.form['duracao']
        posologia.medicamento = MedicamentoModel.query.filter_by(nome=request.form['medicamento']).first()
        posologia.pacientes = PacienteModel.query.filter_by(name=request.form['paciente']).first()
        posologia.usuario = UsuarioModel.query.filter_by(id=session['user_id']).first()
        db.session.add(posologia)
        db.session.commit()

        divisao_dia = 24 / int(posologia.frequencia)
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        for i in range(int(posologia.frequencia) * int(posologia.duracao)):
            horario = HorarioModel()
            horario.data = datetime.now()
            horario.posologias = PosologiaModel.query.filter_by(id_paciente=posologia.pacientes.id).first()
            horario.tomou = False
            horario.hora = datetime.fromtimestamp(ts)
            print(ts)
            print(ts)
            ts += divisao_dia*3600
            db.session.add(horario)
            db.session.commit()
        return redirect(url_for('home'))

    @app.route("/cadastrar_medicamentos", endpoint="cadastrar_medicamentos")
    def buscar_dados():
        medicamentos = MedicamentoModel.query.all()
        pacientes = PacienteModel.query.all()
        if len(medicamentos) == 0:
            tabela = pd.read_excel("./services/basico_20230914.xls")
            tabela = pd.DataFrame.to_numpy(tabela)
            print(tabela)
            for linha in tabela:
                cadastrar_remedio(linha[0])
        return render_template("cadastro_posologia.html", medicamentos=medicamentos, pacientes=pacientes)

    @app.route("/delete/<id>", endpoint="delete_by_id")
    def delete_by_id(id_patient):
        patient = PacienteModel.query.get_or_404(id_patient)
        db.session.delete(patient)
        db.session.commit()
        return redirect(url_for('home'))

    @app.route("/perfil_paciente/<id_patient>", endpoint="perfil_paciente")
    def ver_perfil(id_patient):
        paciente = PacienteModel.query.get_or_404(id_patient)
        posologias = PosologiaModel.query.filter_by(id_paciente=id_patient)
        horarios = []
        for row in posologias:
            horario = HorarioModel.query.filter_by(id_posologia=row.id)
            horarios.append(horario)
        hoje = datetime.now()
        return render_template("perfil_paciente.html", paciente=paciente, posologias=posologias, horarios=horarios, data=hoje)

    @app.route("/mudar_status_tomada/<id_horario>", endpoint="mudar_status_tomada")
    def mudar_status_tomada(id_horario):
        horario = HorarioModel.query.get(id_horario)
        horario.tomou = True
        db.session.commit()
        return ver_perfil(horario.posologias.pacientes.id)

    if __name__ == "__main__":
        app.run()

    return app
