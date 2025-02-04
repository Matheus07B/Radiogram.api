from flask import Flask
from flask_cors import CORS 
from app.models.database import init_db # Importa o banco de dados
from app.routes import register_routes # Importa as rotas
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

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)

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
