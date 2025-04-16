from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.models.user_model import find_user_by_email
from app.models.database import get_db_connection  # Certifique-se de importar corretamente a função
from config import Config
import os

login_blueprint = Blueprint('login', __name__)
SECRET_KEY = os.environ.get("SECRET_KEY")

@login_blueprint.route('', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
        payload = {
            'user_id': usuario["id"],
            'email': usuario["email"],
            'exp': datetime.utcnow() + timedelta(days=365)  # Expira em 1 ano :)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({"mensagem": "Login realizado com sucesso!", "token": token})
    else:
        return jsonify({"erro": "Email ou senha incorretos!"}), 401
