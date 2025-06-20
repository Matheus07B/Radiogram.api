import jwt
import sqlite3
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from app.models.database import get_db_connection
from app.utils.decorators import token_required

# Cria o Blueprint para rotas de chat
chat_blueprint = Blueprint('chat', __name__)

# Rota para deletar mensagem
@chat_blueprint.route('/delete/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verifica se a mensagem é de amigo
        cursor.execute('SELECT * FROM friendMessages WHERE id = ?', (message_id,))
        message = cursor.fetchone()

        if message:
            cursor.execute('DELETE FROM friendMessages WHERE id = ?', (message_id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Mensagem deletada com sucesso (amigo)'}), 200

        # Caso não seja de amigo, verifica se é de grupo
        cursor.execute('SELECT * FROM group_messages WHERE id = ?', (message_id,))
        group_message = cursor.fetchone()

        if group_message:
            cursor.execute('DELETE FROM group_messages WHERE id = ?', (message_id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Mensagem deletada com sucesso (grupo)'}), 200

        # Se não achou em nenhum dos dois
        return jsonify({'error': 'Mensagem não encontrada'}), 404

    except Exception as e:
        print(f"Erro ao deletar mensagem: {e}")
        return jsonify({'error': 'Erro interno'}), 500

    finally:
        conn.close()

# Rota para editar mensagem
@chat_blueprint.route('/edit/<int:message_id>', methods=['PUT'])
@token_required
def edit_message(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    new_content = request.json.get('content')

    # Verifica se a mensagem existe
    cursor.execute('SELECT * FROM friendMessages WHERE id = ?', (message_id,))
    message = cursor.fetchone()

    if message is None:
        conn.close()
        return jsonify({'error': 'Mensagem não encontrada'}), 404

    # Atualiza a mensagem
    cursor.execute('UPDATE friendMessages SET content = ? WHERE id = ?', 
                  (new_content, message_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Mensagem editada com sucesso'}), 200
