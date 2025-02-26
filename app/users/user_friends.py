from flask import Blueprint, jsonify, request
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token
from app.models.database import get_db_connection
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

import jwt

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/list', methods=['GET'])
def list_friends():
    # Obter o token do cabeçalho Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    # Verificar se o cabeçalho está no formato esperado "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        # Extrair o token
        token = auth_header.split(" ")[1]
        # Decodificar o token JWT usando a SECRET_KEY da configuração
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  # Obter o user_id do payload
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Consulta ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
            SELECT u.id, u.nome, u.email
            FROM friendships f
            JOIN usuarios u ON f.friend_id = u.id
            WHERE f.user_id = ?
        ''', (user_id,)
    )
    friends = cursor.fetchall()
    conn.close()

    # Formatar os resultados para retornar como JSON
    friends = [{"id": friend["id"], "nome": friend["nome"], "email": friend["email"]} for friend in friends]
    return jsonify(friends), 200

@friends_blueprint.route('/list/selected', methods=['GET'])
def select_friend_chat():
    # Obter o token do cabeçalho Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    # Verificar se o cabeçalho está no formato esperado "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        # Extrair o token
        token = auth_header.split(" ")[1]
        # Decodificar o token JWT usando a SECRET_KEY da configuração
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  # Obter o user_id do payload
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Obter o ID do amigo a partir dos parâmetros da requisição
    friend_id = request.args.get('friend_id')  # O friend_id será passado como parâmetro na URL
    if not friend_id:
        return jsonify({"error": "friend_id é obrigatório"}), 400

    # Consultar as mensagens entre o usuário autenticado e o amigo
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT m.id, m.message, m.timestamp, m.sender_id, m.receiver_id, m.room
        FROM friendMessages m
        WHERE (m.sender_id = ? AND m.receiver_id = ?)
           OR (m.sender_id = ? AND m.receiver_id = ?)
        ORDER BY m.timestamp
        ''', (user_id, friend_id, friend_id, user_id)
    )
    messages = cursor.fetchall()
    conn.close()

    # Formatar as mensagens para retorno em JSON
    messages_data = [
        {
            "id": message["id"],
            "message": message["message"],
            "timestamp": message["timestamp"],
            "sender_id": message["sender_id"],
            "receiver_id": message["receiver_id"],
            "room": message["room"]
        }
        for message in messages
    ]
    
    return jsonify({"messages": messages_data}), 200

# Remover aqui caso necessario.
@friends_blueprint.route('/list/last', methods=['GET'])
def get_last_message():
    # Obter o token do cabeçalho Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    # Verificar se o cabeçalho está no formato esperado "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        # Extrair o token
        token = auth_header.split(" ")[1]
        # Decodificar o token JWT usando a SECRET_KEY da configuração
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  # Obter o user_id do payload
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Obter o ID do amigo a partir dos parâmetros da requisição
    friend_id = request.args.get('friend_id')  # O friend_id será passado como parâmetro na URL
    if not friend_id:
        return jsonify({"error": "friend_id é obrigatório"}), 400

    # Consultar a última mensagem entre o usuário autenticado e o amigo
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT m.message
        FROM friendMessages m
        WHERE (m.sender_id = ? AND m.receiver_id = ?)
           OR (m.sender_id = ? AND m.receiver_id = ?)
        ORDER BY m.timestamp DESC
        LIMIT 1
        ''', (user_id, friend_id, friend_id, user_id)
    )
    last_message = cursor.fetchone()
    conn.close()

    # Verificar se existe uma mensagem
    if last_message:
        return jsonify({"lastMessage": last_message["message"]}), 200
    else:
        return jsonify({"lastMessage": "Nenhuma mensagem encontrada"}), 404


# Remover aqui caso necessario.

@friends_blueprint.route('/add', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def addFriends():
    return jsonify({"For what": "To add a new friend!"}), 200

@friends_blueprint.route('/LA', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha FROM usuarios')  # Apenas ID, nome e e-mail
    usuarios = cursor.fetchall()
    conn.close()

    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)
