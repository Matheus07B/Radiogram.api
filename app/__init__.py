from flask import Flask
from flask_cors import CORS
from app.models.database import init_db
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurações adicionais (Ex.: secret key)
    app.config.from_object('config')

    # Inicializa o banco de dados
    init_db()

    # Registra as rotas
    register_routes(app)

    return app
