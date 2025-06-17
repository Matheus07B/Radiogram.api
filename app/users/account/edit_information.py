import os
import jwt  # ou flask_jwt_extended se você estiver usando jwt manager
import bcrypt

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

from app.utils.decorators import token_required
from app.models.database import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

edit_blueprint = Blueprint('edit', __name__)

SECRET_KEY = os.environ.get("SECRET_KEY")

@edit_blueprint.route('/profile', methods=['PUT'])
@token_required
def edit_profile():
    try:
        data = request.get_json()
        user_uuid = data.get('userUUID')

        if not user_uuid:
            return jsonify({'error': 'UUID do usuário não fornecido'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica existência
        cursor.execute('SELECT * FROM usuarios WHERE userUUID = ?', (user_uuid,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({'error': 'Usuário não encontrado'}), 404

        # Campos a atualizar
        update_fields = []
        params = []

        if 'nome' in data:
            update_fields.append('nome = ?')
            params.append(data['nome'])

        if 'email' in data:
            update_fields.append('email = ?')
            params.append(data['email'])

        if 'bio' in data:
            update_fields.append('bio = ?')
            params.append(data['bio'])

        if 'telefone' in data:
            update_fields.append('telefone = ?')
            params.append(data['telefone'])

        if 'senha' in data:
            hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            update_fields.append('senha = ?')
            params.append(hashed_password.decode('utf-8'))

        if update_fields:
            query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE userUUID = ?"
            params.append(user_uuid)
            cursor.execute(query, params)
            conn.commit()

        # Busca o usuário atualizado
        cursor.execute('SELECT * FROM usuarios WHERE userUUID = ?', (user_uuid,))
        updated_user = cursor.fetchone()
        conn.close()

        if not updated_user:
            return jsonify({'error': 'Erro ao buscar dados atualizados'}), 500

        usuario = {
            'id': updated_user['id'],
            'nome': updated_user['nome'],
            'email': updated_user['email'],
            'bio': updated_user['bio'],
            'telefone': updated_user['telefone'],
            'userUUID': updated_user['userUUID'],
            'pic': updated_user['pic'],
        }

        payload = {
            'user_id': usuario["id"],
            'nome': usuario["nome"],
            'email': usuario["email"],
            'bio': usuario["bio"],
            'telefone': usuario["telefone"],
            'userUUID': usuario["userUUID"],
            'pic': usuario["pic"],
            'exp': datetime.utcnow() + timedelta(days=365)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'success': True,
            'message': 'Perfil atualizado com sucesso',
            'token': token
        }), 200

    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({'error': 'A atualização não foi concluida!'}), 500
