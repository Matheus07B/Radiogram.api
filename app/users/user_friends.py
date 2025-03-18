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
        SELECT m.id, m.message, m.timestamp, m.sender_id, m.receiver_id
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
            "receiver_id": message["receiver_id"]
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
        SELECT m.message, m.timestamp
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
        mensagem, timestamp = last_message  # Desempacota a tupla
        return jsonify({
            "lastMessage": mensagem,
            "timestamp": timestamp  # Retorna o timestamp corretamente
        }), 200
    else:
        return jsonify({"lastMessage": "Nenhuma mensagem encontrada"}), 404

# Remover aqui caso necessario.

@friends_blueprint.route('/get/room', methods=['GET'])
def get_room():
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

    # Consultar o código da sala entre o usuário autenticado e o amigo
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT r.room_code 
            FROM rooms r
            WHERE (r.user1_id = ? AND r.user2_id = ?) 
            OR (r.user1_id = ? AND r.user2_id = ?)
        """, (user_id, friend_id, friend_id, user_id)
    )
    room = cursor.fetchone()
    conn.close()

    if room:
        # Retorna o código da sala encontrado
        return jsonify({"room_code": room["room_code"]}), 200
    else:
        # Se a sala não for encontrada, retorna erro 404
        return jsonify({"error": "Room not found"}), 404

# Inserir as mensagens no banco de dados.
@friends_blueprint.route('/insert', methods=['POST'])
# @verificar_token  # Protege este endpoint com verificação de token
def insert_message():
    try:
        # Pega os dados da requisição
        data = request.get_json()

        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message = data.get('message')

        if not sender_id or not receiver_id or not message:
            return jsonify({"error": "Faltando informações"}), 400

        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir mensagem na tabela
        cursor.execute('''
            INSERT INTO friendMessages (sender_id, receiver_id, message)
            VALUES (?, ?, ?)
        ''', (sender_id, receiver_id, message))

        conn.commit()

        # Fechar a conexão
        conn.close()

        return jsonify({"status": "Mensagem inserida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
