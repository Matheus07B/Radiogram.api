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

# EMITS de mensagens e etc dos amigos. ================================================
# criptografia
CRYPT_KEY = Fernet.generate_key()
fernet = Fernet(CRYPT_KEY)

def encrypt_message(message: str) -> str:
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

# Mensagens dos amigos.
@socketio.on('message')
def handle_message(data):
    # message = encrypt_message(data.get('message'))
    room = data.get('room')

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
                print(f"[{time}] Sala (Grupo): {room} | De: {user_id} | Mensagem: {message}")
                query = """
                    INSERT INTO group_messages (group_id, sender_id, message, time, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (group_id, user_id, message, time, current_timestamp))
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
    room = data['room']
    image = data['image']  # Imagem recebida em base64
    senderID = data['sender_id']
    friendID = data['friend_id']
    time = data.get('time', "Horário desconhecido")

    try:
        print(f"Imagem recebida na sala {room} às {time}")

        # # Decodificar a imagem base64
        # image_data = base64.b64decode(image_base64.split(',')[1])  # Remove o prefixo 'data:image/...;base64,'
        # files = {'file': ('image.png', BytesIO(image_data), 'image/png')}

        # # Enviar para o backend (armazenar a imagem na nuvem)
        # response = requests.post(STORAGE_API_URL, files=files)

        # if response.status_code == 200:
        #     uploaded_image_url = response.json().get("url")  # URL gerada no backend

        # crypt_image = "https://api.radiogram.shop/upload/download/"+generate_unique_filename(image)
        # print("TESTEEEEEEEEEEEEE - "+ crypt_image) # Somente para debug

        socketio.emit("image", {
            "room": room,
            "image": image,  # URL pública da imagem armazenada (temporária por enquanto)
            "time": time,
            "sender": request.sid
        }, room=room)


        # Conectar ao banco de dados
        cursor = get_db_connection()

        # Query de inserção
        query = "INSERT INTO friendMessages (image, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)"
        data = (image, time, senderID, friendID)

        # Executar a query para salvar a imagem no banco de dados
        cursor.execute(query, data)
        cursor.commit()
        cursor.close()

        print(f"Imagem armazenado: {image}")

    # else:
    #     print(f"Erro ao fazer upload da imagem: {response.text}")

    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")

# Videos.
@socketio.on('video')
def handle_video(data):
    room = data['room']
    video = data['video']
    senderID = data['sender_id']
    friendID = data['friend_id']
    time = data.get('time', "Horário desconhecido")

    try:
        print(f"Vídeo recebido na sala {room}")

        # Decodificação e preparação do arquivo
        # video_data = base64.b64decode(video_base64.split(',')[1])
        # files = {'file': ('video_message.mp4', BytesIO(video_data))}  # Nome genérico

        # # Upload para armazenamento
        # response = requests.post(STORAGE_API_URL, files=files)

        # if response.status_code == 200:
        #     video_url = response.json().get("url")

        # crypt_video = generate_unique_filename(video)

        # Emissão após o update do video na cloud.
        socketio.emit("video", {
            "room": room,
            "video": video,
            "time": time,
            "sender": request.sid,
            "sender_id": senderID,
            "friend_id": friendID
        }, room=room)

        # Persistência no banco (estrutura mínima)
        cursor = get_db_connection()
        cursor.execute(
            "INSERT INTO friendMessages (video, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)",
            (video, time, senderID, friendID)
        )
        cursor.commit()
        cursor.close()

        print(f"Vídeo armazenado: {video}")

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
        document = data['document']
        fileNameEmit = data['fileNameEmit']
        sender_id = data.get('sender_id')
        friend_id = data.get('friend_id')
        time = data.get('time', "Horário desconhecido")

        print(f"Documento recebido na sala {room} às {time}")
        print(f"Nome do arquivo recebido: {fileNameEmit}")

        # # Decodificar o documento base64
        # document_data = base64.b64decode(document_base64.split(',')[1])
        # files = {'file': (file_name, BytesIO(document_data), file_type)}

        # Enviar para o backend de armazenamento
        # response = requests.post(STORAGE_API_URL, files=files)

        # if response.status_code == 200:
        #     uploaded_doc_url = response.json().get("url")

        # document = generate_unique_filename(document)

        socketio.emit("document", {
            "room": room,
            "document": document,
            "fileNameEmit": fileNameEmit,
            "time": time,
            "sender": request.sid,
            "sender_id": sender_id,
            "friend_id": friend_id
        }, room=room)

        # Salvar no banco de dados
        cursor = get_db_connection()
        query = """INSERT INTO friendMessages(document, time, sender_id, receiver_id) VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (document, time, sender_id, friend_id))
        cursor.commit()
        cursor.close()

        print(f"Documento armazenado com sucesso: {document}")

        # else:
        #     print(f"Erro no upload do documento: {response.text}")

    except KeyError as e:
        print(f"Campo obrigatório faltando: {str(e)}")
    except Exception as e:
        print(f"Erro no processamento do documento: {str(e)}")
        import traceback
        traceback.print_exc()
# EMITS de mensagens e etc dos amigos. ================================================

# EMITS de mensagens e etc dos grupos. ================================================
@socketio.on('message-gp')
def handle_group_message(data):
    try:
        room = data.get('room')  # UUID do grupo
        message = data.get('message')
        user_id = data.get('user_id')
        time = data.get('time')

        # Verificação básica de segurança
        if not is_message_safe(message):
            print(f"⚠️ Mensagem bloqueada (conteúdo suspeito): {message}")
            return {"status": "error", "reason": "Conteúdo não permitido"}

        print(f"[{time}] Sala (Grupo): {room} | De: {user_id} | Mensagem: {message}")

        # Envia a mensagem para todos os usuários na sala
        socketio.emit("message", {
            "room": room,
            "message": message,
            "time": time,
            "sender": request.sid
        }, room=room)

        # Insere no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Primeiro pega o ID do grupo com base no UUID
        cursor.execute("SELECT id FROM groups WHERE uuid = ?", (room,))
        group = cursor.fetchone()

        if group:
            group_id = group["id"]

            query = """
                INSERT INTO group_messages (message, time, sender_id, group_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (message, time, user_id, group_id))
            conn.commit()
        else:
            print(f"❌ Grupo com UUID {room} não encontrado no banco.")
            return {"status": "error", "reason": "Grupo não encontrado"}

    except Exception as e:
        print(f"❌ Erro ao processar mensagem do grupo: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
# EMITS de mensagens e etc dos grupos. ================================================            

# Criar a aplicação e rodar o WebSocket
# if __name__ == "__main__":
#     app, socketio = create_app()
#     socketio.run(app, host="127.0.0.1", port=5001, debug=True)
