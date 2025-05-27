from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import uuid  # Importando para gerar UUID
from datetime import datetime, timedelta
from app.models.user_model import find_user_by_email
from app.models.database import get_db_connection  # Certifique-se de importar corretamente a função
import os

register_blueprint = Blueprint('register', __name__)
SECRET_KEY = os.environ.get("SECRET_KEY")

@register_blueprint.route('', methods=['POST'])
def register():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('concatNum')
    senha = dados.get('senha')

    if not nome or not senha or not email:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM usuarios WHERE nome = ? OR email = ?', (nome, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Esse nome de usuário ou email já existe!"}), 400

    user_uuid = str(uuid.uuid4())  # Gerando um UUID único para o usuário

    try:
        cursor.execute(
            'INSERT INTO usuarios (nome, email, telefone, senha, userUUID) VALUES (?, ?, ?, ?, ?)',
            (nome, email, telefone, senha_criptografada, user_uuid)
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!", "userUUID": user_uuid}), 201
