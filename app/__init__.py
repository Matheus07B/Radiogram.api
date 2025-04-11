from flask import Flask
from flask_cors import CORS 
from app.models.database import init_db  # Importa o banco de dados
from app.routes import register_routes  # Importa as rotas
from app.websocket import socketio  # Importa o WebSocket

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Carrega as configurações
    app.config.from_object('config.Config')

    # Inicializa o banco de dados dentro do contexto da app
    with app.app_context():
        init_db()

    # Registra as rotas
    register_routes(app)

    # Inicializa o WebSocket na aplicação Flask
    socketio.init_app(app, cors_allowed_origins="*")

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host="127.0.0.1", port=5001)  # Usando socketio.run() em vez de app.run()

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
