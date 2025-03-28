# import dropbox
# import os
import base64
import requests
import sqlite3

from datetime import datetime
from io import BytesIO

from flask import Flask, request, Blueprint
from flask_socketio import send, emit, join_room, leave_room
from app.websocket import socketio  # Importa a instância global do SocketIO
from app.models.database import get_db_connection

chat_blueprint = Blueprint('chat', __name__)  # Definição do Blueprint

users_rooms = {}  # Mapeia SID do usuário para sua sala atual

@socketio.on('join')
def handle_join(data):
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
    sid = request.sid
    room = data.get('room')

    if sid in users_rooms and users_rooms[sid] == room:
        leave_room(room)
        del users_rooms[sid]
        print(f"Usuário {sid} saiu manualmente da sala {room}")

# Emissão de mensagens.
@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    time = data['time']  # Pega o horário ou usa um padrão

    # Só para debug.
    # print(f"Mensagem na sala {room} às {time}: {message}")

    print(room, message, time)

    # Envia a mensagem de volta para os clientes na sala
    socketio.emit("message", {
        "room": room,
        "message": message,
        "time": time,
        "sender": request.sid
    }, room=room)

# Emissão de fotos.
# Configuração do backend de armazenamento
STORAGE_API_URL = "https://cloud-personal.onrender.com/upload"

@socketio.on('image')
def handle_image(data):
    room = data['room']
    image_base64 = data['image']  # Imagem recebida em base64
    senderID = data['sender_id']
    friendID = data['friend_id']
    time = data.get('time', "Horário desconhecido")

    # Reenviar a imagem para os clientes com a URL real
    socketio.emit("image", {
        "room": room,
        "image": image_base64,  # URL pública da imagem armazenada
        "time": time,
        "sender": request.sid
    }, room=room)

    print(f"Imagem recebida na sala {room} às {time}")

    try:
        # Decodificar a imagem base64
        image_data = base64.b64decode(image_base64.split(',')[1])  # Remove o prefixo 'data:image/...;base64,'
        files = {'file': ('image.png', BytesIO(image_data), 'image/png')}

        # Enviar para o backend
        response = requests.post(STORAGE_API_URL, files=files)

        if response.status_code == 200:
            uploaded_image_url = response.json().get("url")  # URL gerada no backend

            cursor = get_db_connection()

            # Query de inserção
            query = "INSERT INTO friendMessages (image, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)"
            data = (
                uploaded_image_url,
                time,
                senderID,
                friendID
            )

            cursor.execute(query, data)
            cursor.commit()
            cursor.close()

            # Debug print
            # print("Imagem inserida com sucesso, link: "+ uploaded_image_url)

        else:
            print(f"Erro ao fazer upload da imagem: {response.text}")
    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")

# Emissão de documentos.
@socketio.on('document')
def handle_document(data):
    room = data['room']
    document_data = data['document']
    time = data.get('time', "Horário desconhecido")  # Pega o horário ou usa um padrão
    
    print(f"Documento recebido na sala {room} às {time}")

    # Reenvia para todos os clientes na sala
    socketio.emit("document", {
        "room": room,
        "document": document_data,
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