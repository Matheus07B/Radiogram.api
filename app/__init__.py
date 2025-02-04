from flask import Flask
from flask_cors import CORS
from app.models.database import init_db
from app.routes import register_routes
from app.websocket.web_chat import configure_websocket  # Importa o WebSocket

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Carrega as configurações
    app.config.from_object('config.Config')  # Certifique-se de referenciar a classe Config corretamente

    # Inicializa o banco de dados dentro do contexto da app
    with app.app_context():
        init_db()

    # Registra as rotas
    register_routes(app)

    # Configura o WebSocket dentro da API
    socketio = configure_websocket(app)

    return app, socketio  # Retorna o WebSocket junto com a app

##############################################################################

# from flask import Flask
# from flask_cors import CORS
# from app.models.database import init_db
# from app.routes import register_routes

# def create_app():
#     app = Flask(__name__)
#     CORS(app)

#     # Carrega as configurações
#     app.config.from_object('config.Config')  # Certifique-se de referenciar a classe Config corretamente

#     # Inicializa o banco de dados dentro do contexto da app
#     with app.app_context():
#         init_db()

#     # Registra as rotas
#     register_routes(app)

#     return app
