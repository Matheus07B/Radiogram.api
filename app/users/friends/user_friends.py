import jwt
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import Config
from app.models.user_model import get_all_users
from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import friends_blueprint

@friends_blueprint.route('/list', methods=['GET'])
@token_required
def list_friends():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Buscar amigos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.id, u.nome, u.email, u.telefone, u.userUUID, u.bio, u.pic
        FROM friendships f
        JOIN usuarios u ON f.friend_id = u.id
        WHERE f.user_id = ?
    ''', (user_id,))
    friends = cursor.fetchall()
    conn.close()

    # Buscar grupos
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT g.id, g.name, g.uuid
        FROM groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.user_id = ?
    """, (user_id,))
    grupos = cur.fetchall()
    con.close()

    # Formatar amigos
    friends_data = [{
        "id": friend["id"],
        "nome": friend["nome"],
        "email": friend["email"],
        "telefone": friend["telefone"],
        "userUUID": friend["userUUID"],
        "bio": friend["bio"],
        "pic": friend["pic"]
    } for friend in friends]

    # Formatar grupos com UUID incluído
    grupos_data = [{
        "id": grupo[0],
        "name": grupo[1],
        "uuid": grupo[2]
    } for grupo in grupos]

    # Resposta final com amigos e grupos
    return jsonify({
        "friends": friends_data,
        "groups": grupos_data
    }), 200

@friends_blueprint.route('/list/selected', methods=['GET'])
@token_required
def select_friend_chat():
    # Verificação do token (mantido igual)
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token inválido ou faltando"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    friend_id = request.args.get('friend_id')
    if not friend_id:
        return jsonify({"error": "friend_id é obrigatório"}), 400

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Consultar o código da sala entre o usuário autenticado e o amigo
        cursor.execute(
            """
                SELECT r.room_code 
                FROM rooms r
                WHERE (r.user1_id = ? AND r.user2_id = ?) 
                OR (r.user1_id = ? AND r.user2_id = ?)
            """, (user_id, friend_id, friend_id, user_id)
        )
        room = cursor.fetchone()

        if not room:
            return jsonify({"error": "Room not found"}), 404

        room_code = room["room_code"]

        # Buscar mensagens entre os dois usuários
        cursor.execute(
            '''
            SELECT 
                m.id, 
                m.message, 
                m.image, 
                m.video,
                m.document,
                m.time, 
                m.sender_id, 
                m.receiver_id
            FROM friendMessages m
            WHERE (m.sender_id = ? AND m.receiver_id = ?)
               OR (m.sender_id = ? AND m.receiver_id = ?)
            ORDER BY m.timestamp
            ''', (user_id, friend_id, friend_id, user_id)
        )
        messages = cursor.fetchall()

        messages_data = []
        for message in messages:
            msg_data = {
                "id": message["id"],
                "message": message["message"],
                "time": message["time"],
                "sender_id": message["sender_id"],
                "receiver_id": message["receiver_id"]
            }

            if message["image"]:
                msg_data["image_url"] = f"{message['image']}"
            
            if message["video"]:
                msg_data["video"] = f"{message['video']}"

            if message["document"]:
                msg_data["document"] = message['document']

            messages_data.append(msg_data)

        return jsonify({
            "room_code": room_code,
            "messages": messages_data
        }), 200

    except Exception as e:
        print(f"Erro no banco de dados: {str(e)}")
        return jsonify({"error": "Erro interno"}), 500

    finally:
        conn.close()

# Remover aqui caso necessario.
@friends_blueprint.route('/list/last', methods=['GET'])
@token_required
def get_last_message():
    # Obter o token do cabeçalho Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    # Verificar se o cabeçalho está no formato esperado "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        # Extrair e decodificar o token JWT
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Obter o ID do amigo a partir dos parâmetros da requisição
    friend_id = request.args.get('friend_id')
    if not friend_id:
        return jsonify({"error": "friend_id é obrigatório"}), 400

    # Consultar a última mensagem entre o usuário autenticado e o amigo
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
    '''
        SELECT m.message, m.time
        FROM friendMessages m
        WHERE (m.sender_id = ? AND m.receiver_id = ?)
        OR (m.sender_id = ? AND m.receiver_id = ?)
        ORDER BY m.timestamp DESC, m.id DESC
        LIMIT 1
    ''', (user_id, friend_id, friend_id, user_id)
    )
    last_message = cursor.fetchone()
    conn.close()

    # Verificar se existe uma mensagem
    if last_message:
        mensagem, time = last_message  # Desempacota a tupla
        return jsonify({
            "lastMessage": mensagem, # Retorna a última mensagem
            "time": time  # Retorna a hota da ultima mensagem, ex: 13:40
        }), 200
    else:
        return jsonify({
            "lastMessage": "",
            "time": ""
        }), 404

# @friends_blueprint.route('/LA', methods=['GET'])
# @token_required
# def listar_usuarios():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, nome, email, senha FROM usuarios')  # Apenas ID, nome e e-mail
#     usuarios = cursor.fetchall()
#     conn.close()

#     resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
#     return jsonify(resultado)