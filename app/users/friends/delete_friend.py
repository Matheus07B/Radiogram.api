import re
import uuid

from flask import Blueprint, jsonify, request

from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import friends_blueprint

@friends_blueprint.route('/delete', methods=['POST'])
@token_required
def delete_friend():
    data = request.get_json()

    friend_number = data.get("friendNumber")  # Telefone do amigo
    user_id = data.get("currentUserId")       # ID do usuário atual

    print(f"Número de celular do amigo: {friend_number}")
    print(f"ID do usuário que requisitou a amizade: {user_id}")

    PHONE_REGEX = re.compile(r'^(55)?[1-9]{2}9\d{8}$')  # Aceita DDDs válidos e celular com 9 dígitos

    if not friend_number or not user_id:
        return jsonify({"message": "Dados insuficientes."}), 400

    # Validação: celular deve ter DDD (2 dígitos de 1-9) e começar com 9, seguido de 8 dígitos
    if not PHONE_REGEX.fullmatch(friend_number):
        return jsonify({"message": "Número de celular inválido. Ex: 11912345678 ou 5511912345678"}), 400

    try:
        # Insert na amizade ========
        conn = get_db_connection()
        cursor = conn.cursor()

        # Busca o ID do amigo com base no número de telefone
        cursor.execute('SELECT id FROM usuarios WHERE telefone = ?', (friend_number,))
        friendResult = cursor.fetchone()

        if not friendResult:
            return jsonify({"message": "Amigo não encontrado com esse número."}), 404

        friend_id = friendResult['id']

        # Insere amizade em ambos os sentidos
        cursor.executemany(
            'INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)',
            [
                (user_id, friend_id),
                (friend_id, user_id)
            ]
        )

        conn.commit()

        # Insert na sala ========
        cursor = conn.cursor()
        room_UUID = str(uuid.uuid4())  # Gerando um UUID único para a sala

        roomQuery = """INSERT INTO rooms (room_code, user1_id, user2_id) VALUES (?, ?, ?)"""
        cursor.execute(roomQuery, (room_UUID, user_id, friend_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "Amizade criada com sucesso!"}), 201

    except Exception as e:
        print("Erro ao inserir amizade:", e)
        return jsonify({"message": "Erro ao adicionar amizade."}), 500
