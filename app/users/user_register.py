from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.models.user_model import find_user_by_email
from app.models.database import get_db_connection  # Certifique-se de importar corretamente a função
import os

register_blueprint = Blueprint('register', __name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "minha-chave-secreta")

@register_blueprint.route('', methods=['POST'])
def register():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')

    if not nome or not senha or not email:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM usuarios WHERE nome = ? OR email = ?', (nome, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Esse nome de usuário ou email já existe!"}), 400

    try:
        cursor.execute(
            'INSERT INTO usuarios (nome, senha, email) VALUES (?, ?, ?)',
            (nome, senha_criptografada, email)
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 201