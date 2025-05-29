from flask import Blueprint, jsonify, request
from app.models.database import get_db_connection

add_friend_blueprint = Blueprint('addfriend', __name__)

@add_friend_blueprint.route('', methods=['POST'])
def add_friend():
    data = request.get_json()

    friend_number = data.get("friendNumber")  # Telefone do amigo
    user_id = data.get("currentUserId")       # ID do usuário atual

    print(f"Número de celular do amigo: {friend_number}")
    print(f"ID do usuário que requisitou a amizade: {user_id}")

    if not friend_number or not user_id:
        return jsonify({"message": "Dados insuficientes."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Busca o ID do amigo com base no número de telefone
        cursor.execute('SELECT id FROM usuarios WHERE telefone = ?', (friend_number,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "Amigo não encontrado com esse número."}), 404

        friend_id = result['id']

        # Insere amizade em ambos os sentidos
        cursor.executemany(
            'INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)',
            [
                (user_id, friend_id),
                (friend_id, user_id)
            ]
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Amizade criada com sucesso!"}), 201

    except Exception as e:
        print("Erro ao inserir amizade:", e)
        return jsonify({"message": "Erro ao adicionar amizade."}), 500
