import sqlite3
from flask import Flask, request, Blueprint
from flask_socketio import send, emit, join_room, leave_room
from app.websocket import socketio  # Importa a instância global do SocketIO

chat_blueprint = Blueprint('chat', __name__)  # Definição do Blueprint

# Função para conectar ao banco de dados
def get_db():
    conn = sqlite3.connect('chat.db')  # Conecte-se ao banco de dados
    conn.row_factory = sqlite3.Row  # Para retornar dicionários
    return conn

users_rooms = {}  # Mapeia SID do usuário para sua sala atual

@socketio.on('join')
def handle_join(data):
    """Gerencia a entrada do usuário em uma sala."""
    username = data['username']
    new_room = data['room']
    sid = request.sid

    if sid in users_rooms:
        old_room = users_rooms[sid]
        leave_room(old_room)
        print(f"Usuário {username} saiu da sala {old_room}")

    users_rooms[sid] = new_room
    join_room(new_room)
    print(f"Usuário {username} entrou na sala {new_room}")

@socketio.on('leave')
def handle_leave(data):
    """Gerencia a saída do usuário de uma sala."""
    sid = request.sid
    room = data.get('room')

    if sid in users_rooms and users_rooms[sid] == room:
        leave_room(room)
        del users_rooms[sid]
        print(f"Usuário {sid} saiu manualmente da sala {room}")

@socketio.on('message')
def handle_message(data):
    """Gerencia mensagens e imagens enviadas no chat."""
    room = data['room']
    message = data['message']
    image = request.files.get("image", None)  # Obtém a imagem enviada (se houver)
    time = data.get('time', '00:00')  # Pega o horário ou usa um padrão

    image_url = None
    if image:
        # Converte a imagem para binário
        image_data = image.read()  # Lê a imagem como binário

        # Armazena a imagem no banco de dados
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO friendMessages (sender_id, receiver_id, message, image)
            VALUES (?, ?, ?, ?)
        """, (sender_id, receiver_id, None, image_data))  # A mensagem fica como NULL se for apenas imagem
        conn.commit()
        conn.close()

        image_url = "/path/to/serve/image"  # Defina a URL para servir a imagem, caso necessário

    print(f"Mensagem na sala {room} às {time}: {message or '[Imagem]'}")

    # Envia a mensagem com ou sem imagem
    socketio.emit("message", {
        "room": room,
        "message": message,
        "image": image_url,
        "time": time,
        "sender": request.sid
    }, room=room)

# Criar a aplicação e rodar o WebSocket
# if __name__ == "__main__":
#     app, socketio = create_app()
#     socketio.run(app, host="127.0.0.1", port=5001, debug=True)



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