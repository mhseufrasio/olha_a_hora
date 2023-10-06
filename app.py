import os

from flask_oauthlib.provider import OAuth2Provider
from flask import Flask, json, render_template
from flask_migrate import Migrate
from flask_smorest import Api
from db import db
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from controllers.patient import blp as PatientBlueprint


def create_app(db_url=None):
    app = Flask(__name__, template_folder="templates")

    @app.route("/")
    def index():
        return render_template('index.html')

    if __name__ == "__main__":
        app.run()

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
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(PatientBlueprint)
    return app
