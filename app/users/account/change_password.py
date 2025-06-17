from flask import Blueprint, request, jsonify
from app.models.database import get_db_connection
import bcrypt  # mais seguro que hashlib

change_password_blueprint = Blueprint('changepassword', __name__)

@change_password_blueprint.route('', methods=['POST'])
def trocar_senha():
    email = request.json.get('email')
    nova_senha = request.json.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({"erro": "Email e nova senha são obrigatórios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se há código de recuperação para o email
        query = "SELECT * FROM recoverCodes WHERE email = ?"
        cursor.execute(query, (email,))
        resultado = cursor.fetchone()

        if resultado:
            # Gera o hash da nova senha com bcrypt
            senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt())

            # Atualiza a senha na tabela usuarios
            update_query = "UPDATE usuarios SET senha = ? WHERE email = ?"
            cursor.execute(update_query, (senha_hash, email))

            # Remove o código de recuperação
            delete_query = "DELETE FROM recoverCodes WHERE email = ?"
            cursor.execute(delete_query, (email,))

            conn.commit()
            mensagem = {"mensagem": "Senha atualizada com sucesso!"}
            status = 200
        else:
            mensagem = {"erro": "Código inválido ou expirado"}
            status = 401

        cursor.close()
        conn.close()
        return jsonify(mensagem), status

    except Exception as e:
        # return jsonify({"erro": f"Erro no servidor: {str(e)}"}), 500
        return jsonify({"erro": "erro interno!"}), 500
