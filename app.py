""" Aplicação em Flask Para o Controle de Horários de Tomada de Remédios"""
import os
import pathlib

import requests
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow

from flask import Flask, render_template, request, url_for, redirect, session, abort
from flask_smorest import Api
from dotenv import load_dotenv
from pip._vendor import cachecontrol
from google.oauth2 import id_token
from db import db
from controllers.patient import blp as PatientBlueprint
from models import PacienteModel


def create_app(db_url=None):
    """Configurações da Aplicação e Rotas de Acesso"""
    app = Flask(__name__, template_folder="templates")
    load_dotenv()
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

    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="http://127.0.0.1:5000/login/callback"
    )

    def login_is_required(function):
        if "google_id" not in session:
            return render_template('login.html')
        return function()

    @app.route("/", endpoint="index")
    def index():
        return render_template('login.html')

    @app.route("/home", endpoint="home")
    @login_is_required
    def home():
        all_patients = PacienteModel.query.all()
        return render_template('index.html', patients=all_patients)

    @app.route("/login")
    def login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    @app.route("/logout", endpoint="logout")
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route("/login/callback", endpoint="google_callback")
    def callback():
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience="769885220922-1mrnk17gnvu5oel23g95p0cn0r3uea02.apps.googleusercontent.com"
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return redirect(url_for('home'))

    @app.route("/add_patient", methods=["POST"], endpoint="add_patient")
    @login_is_required
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
    @login_is_required
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

    api.register_blueprint(PatientBlueprint)
    return app
