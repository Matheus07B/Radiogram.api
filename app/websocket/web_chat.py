from flask import Flask, Blueprint, request, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os

socketio = SocketIO(cors_allowed_origins="*")  # Criar a instância do SocketIO

# web_chat_blueprint = Blueprint('web_chat', __name__)
# @web_chat_blueprint.route('')

def configure_websocket(app):
    """Configurar WebSocket dentro da API Flask"""
    socketio.init_app(app)

    @socketio.on('connect')
    def handle_connect():
        print("Cliente conectado")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Cliente desconectado")

    @socketio.on('message')
    def handle_message(data):
        print(f"Mensagem recebida: {data}")
        send(data, broadcast=True)

    @socketio.on('join')
    def handle_join(data):
        room = data['room']
        join_room(room)
        emit('message', f"Entrou na sala: {room}", room=room)

    @socketio.on('leave')
    def handle_leave(data):
        room = data['room']
        leave_room(room)
        emit('message', f"Saiu da sala: {room}", room=room)

    return socketio


################################################################

# from flask import Flask, Blueprint, request, jsonify
# from flask_socketio import SocketIO, send, emit, join_room, leave_room
# from flask_cors import CORS
# import os

# app = Flask(__name__)

# web_chat_blueprint = Blueprint('web_chat', __name__)
# SECRET_KEY = os.environ.get("SECRET_KEY", "minha-chave-secreta")

# CORS(app)  # Permitir origens diferentes (se necessário)

# # Configurar SocketIO para permitir CORS
# socketio = SocketIO(app, cors_allowed_origins="*")  # "*" permite todas as origens

# # Rota principal para o site
# @web_chat_blueprint.route('')
# def index():
#     return "Servidor WebSocket em execução"

# # Evento de conexão
# @socketio.on('connect', namespace='/web_chat')
# def handle_connect():
#     print("Cliente conectado")

# # Evento de desconexão
# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Cliente desconectado")

# # Receber e enviar mensagens para todos
# @socketio.on('message')
# def handle_message(data):
#     print(f"Mensagem recebida: {data}")
#     send(data, broadcast=True)  # Envia a mensagem para todos os clientes conectados

# # Sistema de salas (para chats privados ou grupos)
# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     join_room(room)
#     emit('message', f"Entrou na sala: {room}", room=room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     leave_room(room)
#     emit('message', f"Saiu da sala: {room}", room=room)

# if __name__ == '__main__':
#     socketio.run(app, debug=True, host="0.0.0.0", port=5001)


#############################################################################################


# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, send, emit, join_room, leave_room
# from flask_cors import CORS

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Defina uma chave secreta para a sessão
# CORS(app)  # Permitir origens diferentes (se necessário)

# # Configurar SocketIO para permitir CORS
# socketio = SocketIO(app, cors_allowed_origins="*")  # "*" permite todas as origens

# # Rota principal para verificação
# @app.route('/')
# def index():
#     return jsonify({"message": "API WebSocket ativa e em execução"}), 200

# # Rota adicional para teste (HTTP)
# @app.route('/api/test', methods=['GET'])
# def test_api():
#     return jsonify({"message": "Esta é uma rota de teste HTTP"}), 200

# # WebSocket: evento de conexão
# @socketio.on('connect')
# def handle_connect():
#     print("Cliente conectado")
#     emit('message', {"message": "Bem-vindo ao servidor WebSocket!"})

# # WebSocket: evento de desconexão
# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Cliente desconectado")

# # WebSocket: evento para mensagens de broadcast
# @socketio.on('message')
# def handle_message(data):
#     print(f"Mensagem recebida: {data}")
#     send({"message": data.get("message", ""), "user": data.get("user", "Anon")}, broadcast=True)

# # WebSocket: gerenciar salas de chat
# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     join_room(room)
#     emit('message', {"message": f"Entrou na sala: {room}", "user": data.get("user", "Anon")}, room=room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     leave_room(room)
#     emit('message', {"message": f"Saiu da sala: {room}", "user": data.get("user", "Anon")}, room=room)

# # Iniciar servidor
# if __name__ == '__main__':
#     socketio.run(app, debug=True, host="127.0.0.1", port=5001)