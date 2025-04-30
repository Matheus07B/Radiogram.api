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

# Configuração do backend de armazenamento
STORAGE_API_URL = "https://cloud-personal.onrender.com/upload"

# Entra na sala
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

# Sai da sala
@socketio.on('leave')
def handle_leave(data):
    sid = request.sid
    room = data.get('room')

    if sid in users_rooms and users_rooms[sid] == room:
        leave_room(room)
        del users_rooms[sid]
        print(f"Usuário {sid} saiu manualmente da sala {room}")

# EMITS de mensagens e etc. ================================================
# Mensagens
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

# Fotos.
@socketio.on('image')
def handle_image(data):
    room = data['room']
    image_base64 = data['image']  # Imagem recebida em base64
    senderID = data['sender_id']
    friendID = data['friend_id']
    time = data.get('time', "Horário desconhecido")

    try:
        print(f"Imagem recebida na sala {room} às {time}")

        # Decodificar a imagem base64
        image_data = base64.b64decode(image_base64.split(',')[1])  # Remove o prefixo 'data:image/...;base64,'
        files = {'file': ('image.png', BytesIO(image_data), 'image/png')}

        # Enviar para o backend (armazenar a imagem na nuvem)
        response = requests.post(STORAGE_API_URL, files=files)

        if response.status_code == 200:
            uploaded_image_url = response.json().get("url")  # URL gerada no backend

            socketio.emit("image", {
                "room": room,
                "image": uploaded_image_url,  # URL pública da imagem armazenada (temporária por enquanto)
                "time": time,
                "sender": request.sid
            }, room=room)

            # Conectar ao banco de dados
            cursor = get_db_connection()

            # Query de inserção
            query = "INSERT INTO friendMessages (image, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)"
            data = (uploaded_image_url, time, senderID, friendID)

            # Executar a query para salvar a imagem no banco de dados
            cursor.execute(query, data)
            cursor.commit()
            cursor.close()

            print("Imagem inserida com sucesso, link: " + uploaded_image_url)

        else:
            print(f"Erro ao fazer upload da imagem: {response.text}")

    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")

# Videos.
@socketio.on('video')
def handle_video(data):
    room = data['room']
    video_base64 = data['video']
    senderID = data['sender_id']
    friendID = data['friend_id']
    time = data.get('time', "Horário desconhecido")

    try:
        print(f"Vídeo recebido na sala {room}")

        # Decodificação e preparação do arquivo
        video_data = base64.b64decode(video_base64.split(',')[1])
        files = {'file': ('video_message.mp4', BytesIO(video_data))}  # Nome genérico

        # Upload para armazenamento
        response = requests.post(STORAGE_API_URL, files=files)

        if response.status_code == 200:
            video_url = response.json().get("url")

            # Emissão após o update do video na cloud.
            socketio.emit("video", {
                "room": room,
                "video": video_url,
                "time": time,
                "sender": request.sid,
                "sender_id": senderID,
                "friend_id": friendID
            }, room=room)

            # Persistência no banco (estrutura mínima)
            cursor = get_db_connection()
            cursor.execute(
                "INSERT INTO friendMessages (video, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)",
                (video_url, time, senderID, friendID)
            )
            cursor.commit()
            cursor.close()

            print(f"Vídeo armazenado: {video_url}")

    except Exception as e:
        print(f"Erro no vídeo: {str(e)}")
        socketio.emit('video_error', {
            'message': 'Falha no processamento',
            'room': room
        }, room=room)

# Documentos
@socketio.on('document')
def handle_document(data):
    try:
        room = data['room']
        document_base64 = data['document']
        file_name = data.get('name', 'document')
        file_type = data.get('type', 'application/octet-stream')
        sender_id = data.get('sender_id')
        friend_id = data.get('friend_id')
        time = data.get('time', "Horário desconhecido")

        print(f"Documento recebido na sala {room} às {time}")

        # Decodificar o documento base64
        document_data = base64.b64decode(document_base64.split(',')[1])
        files = {'file': (file_name, BytesIO(document_data), file_type)}

        # Enviar para o backend de armazenamento
        response = requests.post(STORAGE_API_URL, files=files)

        if response.status_code == 200:
            uploaded_doc_url = response.json().get("url")

            socketio.emit("document", {
                "room": room,
                "document": document_base64,
                "name": file_name,
                "type": file_type,
                "time": time,
                "sender": request.sid,
                "sender_id": sender_id,
                "friend_id": friend_id
            }, room=room)

            # Salvar no banco de dados
            cursor = get_db_connection()
            query = """INSERT INTO friendMessages(document, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)"""
            cursor.execute(query, (uploaded_doc_url, time, sender_id, friend_id))
            cursor.commit()
            cursor.close()

            print(f"Documento armazenado com sucesso: {uploaded_doc_url}")

        else:
            print(f"Erro no upload do documento: {response.text}")

    except KeyError as e:
        print(f"Campo obrigatório faltando: {str(e)}")
    except Exception as e:
        print(f"Erro no processamento do documento: {str(e)}")
        import traceback
        traceback.print_exc()
# ================================================

# Criar a aplicação e rodar o WebSocket
# if __name__ == "__main__":
#     app, socketio = create_app()
#     socketio.run(app, host="127.0.0.1", port=5001, debug=True)
