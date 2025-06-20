# import dropbox
import os
import uuid
import base64
import sqlite3
import hashlib
import requests

from io import BytesIO
from datetime import datetime
from cryptography.fernet import Fernet
from flask import Flask, request, Blueprint
from flask_socketio import send, emit, join_room, leave_room

from app.websocket import socketio  # Importa a instância global do SocketIO
from app.models.database import get_db_connection
from app.websocket.security.check_message import is_message_safe

# websocket_blueprint = Blueprint('chat', __name__)
websocket_blueprint = Blueprint('websocket', __name__)

users_rooms = {}  # Mapeia SID do usuário para sua sala atual

# Configuração do backend de armazenamento
STORAGE_API_URL = os.getenv('STORAGE_API_URL')

def generate_unique_filename(filename):
    """Gera um nome único baseado em UUID + hash"""
    ext = os.path.splitext(filename)[1]  # Pega a extensão original
    unique_id = str(uuid.uuid4())  # Gera um UUID único
    hash_part = hashlib.sha256(unique_id.encode()).hexdigest()[:16]  # Hash de 16 caracteres
    return f"{unique_id}_{hash_part}{ext}"  # Ex: 550e8400-e29b-41d4-a716_4f3c2a8e9b1d.jpg"

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
    # print(f"Usuário {username} entrou na sala {new_room}")

# Sai da sala
@socketio.on('leave')
def handle_leave(data):
    sid = request.sid
    room = data.get('room')

    if sid in users_rooms and users_rooms[sid] == room:
        leave_room(room)
        del users_rooms[sid]
        print(f"Usuário {sid} saiu manualmente da sala {room}")

# EMITS de mensagens e etc dos amigos. ================================================
# criptografia
CRYPT_KEY = Fernet.generate_key()
fernet = Fernet(CRYPT_KEY)

def encrypt_message(message: str) -> str:
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

# Mensagens.
@socketio.on('message')
def handle_message(data):
    # message = encrypt_message(data.get('message'))
    try:
        room = data.get('room')
        message = data.get('message')
        user_id = data.get('user_id')
        friend_id = data.get('friend_id')
        time = data.get('time')

        # Verificação de segurança
        if not is_message_safe(message):
            print(f"⚠️ Mensagem bloqueada (conteúdo suspeito): {message}")
            return {"status": "error", "reason": "Conteúdo não permitido"}

        if friend_id is None:
            # print(f"⚠️ ERRO: friend_id está None! Payload recebido: {data}")
            # friend_id = "1312312"
            # return {"status": "error", "reason": "friend_id ausente no chat privado"}
            return

        # Envia a mensagem para todos na sala (evento padrão)
        socketio.emit("message", {
            "room": room,
            "message": message,
            "time": time,
            "sender": request.sid
        }, room=room)

        # Conexão com o banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Primeiro tenta verificar se é uma sala privada (amigos)
        cursor.execute("SELECT * FROM rooms WHERE room_code = ?", (room,))
        private_result = cursor.fetchone()

        if private_result:
            print(f"[{time}] Sala (Amigo): {room} | De: {user_id} Para: {friend_id} | Mensagem: {message}")
            query = """
                INSERT INTO friendMessages (message, time, sender_id, receiver_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (message, time, user_id, friend_id))

        else:
            # Se não for privado, tenta ver se é grupo
            cursor.execute("SELECT * FROM groups WHERE uuid = ?", (room,))
            group_result = cursor.fetchone()

            if group_result:
                group_id = group_result["id"]
                print(f"[{time}] Sala (Grupo): {room} | De: {user_id} para {friend_id} | Mensagem: {message}")
                query = """
                    INSERT INTO group_messages (group_id, sender_id, receiver_uuid, message, time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (group_id, user_id, friend_id, message, time, current_timestamp))
            else:
                print("⚠️ Sala não encontrada: nem grupo nem amigos.")
                return {"status": "error", "reason": "Sala inválida"}

        conn.commit()

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# Fotos.
@socketio.on('image')
def handle_image(data):
    try:
        room = data['room']
        image = data['image']  # Imagem recebida em base64
        senderID = data['sender_id']
        friendID = data['friend_id']
        time = data.get('time', "Horário desconhecido")

        # Verificação de segurança simples
        if not image:
            print("⚠️ Imagem vazia recebida, ignorando.")
            return

        # Emite para todos da sala
        socketio.emit("image", {
            "room": room,
            "image": image,
            "time": time,
            "sender": request.sid
        }, room=room)

        # Conectar ao banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Primeiro tenta verificar se é uma sala privada (amigos)
        cursor.execute("SELECT * FROM rooms WHERE room_code = ?", (room,))
        private_result = cursor.fetchone()

        if private_result:
            print(f"[{time}] 📸 Sala (Amigo): {room} | De: {senderID} Para: {friendID}")
            query = """
                INSERT INTO friendMessages (image, time, sender_id, receiver_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (image, time, senderID, friendID))

        else:
            # Verifica se é grupo
            cursor.execute("SELECT * FROM groups WHERE uuid = ?", (room,))
            group_result = cursor.fetchone()

            if group_result:
                group_id = group_result["id"]
                print(f"[{time}] 📸 Sala (Grupo): {room} | De: {senderID}")
                query = """
                    INSERT INTO group_messages (group_id, sender_id, receiver_uuid, image, time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (group_id, senderID, friendID, image, time, current_timestamp))
            else:
                print("⚠️ Sala não encontrada: nem grupo nem amigos.")
                return {"status": "error", "reason": "Sala inválida"}

        conn.commit()

    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# Videos.
@socketio.on('video')
def handle_video(data):
    try:
        room = data['room']
        video = data['video']
        senderID = data['sender_id']
        friendID = data['friend_id']
        time = data.get('time', "Horário desconhecido")

        # Verificação básica
        if not video:
            print("⚠️ Vídeo vazio recebido, ignorando.")
            return

        # Emissão para a sala
        socketio.emit("video", {
            "room": room,
            "video": video,
            "time": time,
            "sender": request.sid,
            "sender_id": senderID,
            "friend_id": friendID
        }, room=room)

        # Conexão com banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se é sala de amigo
        cursor.execute("SELECT * FROM rooms WHERE room_code = ?", (room,))
        private_result = cursor.fetchone()

        if private_result:
            print(f"[{time}] 🎥 Sala (Amigo): {room} | De: {senderID} Para: {friendID}")
            query = """
                INSERT INTO friendMessages (video, time, sender_id, receiver_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (video, time, senderID, friendID))

        else:
            # Verifica se é grupo
            cursor.execute("SELECT * FROM groups WHERE uuid = ?", (room,))
            group_result = cursor.fetchone()

            if group_result:
                group_id = group_result["id"]
                print(f"[{time}] 🎥 Sala (Grupo): {room} | De: {senderID}")
                query = """
                    INSERT INTO group_messages (group_id, sender_id, receiver_uuid, video, time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (group_id, senderID, friendID, video, time, current_timestamp))
            else:
                print("⚠️ Sala não encontrada: nem grupo nem amigos.")
                return {"status": "error", "reason": "Sala inválida"}

        conn.commit()

    except Exception as e:
        print(f"Erro no vídeo: {str(e)}")
        socketio.emit('video_error', {
            'message': 'Falha no processamento',
            'room': room
        }, room=room)

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# Documentos
@socketio.on('document')
def handle_document(data):
    try:
        room = data['room']
        document = data['document']
        fileNameEmit = data['fileNameEmit']
        sender_id = data.get('sender_id')
        friend_id = data.get('friend_id')
        time = data.get('time', "Horário desconhecido")

        if not document:
            print("⚠️ Documento vazio recebido, ignorando.")
            return

        print(f"📄 Documento recebido na sala {room} às {time} | Nome: {fileNameEmit}")

        # Emitir para os usuários na sala
        socketio.emit("document", {
            "room": room,
            "document": document,
            "fileNameEmit": fileNameEmit,
            "time": time,
            "sender": request.sid,
            "sender_id": sender_id,
            "friend_id": friend_id
        }, room=room)

        # Conexão com banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se é sala de amigo
        cursor.execute("SELECT * FROM rooms WHERE room_code = ?", (room,))
        private_result = cursor.fetchone()

        if private_result:
            print(f"[{time}] 📄 Sala (Amigo): {room} | De: {sender_id} Para: {friend_id}")
            query = """
                INSERT INTO friendMessages (document, time, sender_id, receiver_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (document, time, sender_id, friend_id))

        else:
            # Verifica se é grupo
            cursor.execute("SELECT * FROM groups WHERE uuid = ?", (room,))
            group_result = cursor.fetchone()

            if group_result:
                group_id = group_result["id"]
                print(f"[{time}] 📄 Sala (Grupo): {room} | De: {sender_id}")
                query = """
                    INSERT INTO group_messages (group_id, sender_id, receiver_uuid, document, time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (group_id, sender_id, friend_id, document, time, current_timestamp))
            else:
                print("⚠️ Sala não encontrada: nem grupo nem amigos.")
                return {"status": "error", "reason": "Sala inválida"}

        conn.commit()

    except KeyError as e:
        print(f"Campo obrigatório faltando: {str(e)}")
    except Exception as e:
        print(f"Erro no processamento do documento: {str(e)}")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# import traceback
# traceback.print_exc()

# EMITS de mensagens e etc dos amigos. ================================================

# Criar a aplicação e rodar o WebSocket
# if __name__ == "__main__":
#     app, socketio = create_app()
#     socketio.run(app, host="127.0.0.1", port=5001, debug=True)
