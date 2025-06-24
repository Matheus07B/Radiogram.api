import os
import re
import jwt
import bcrypt
import base64 # Import base64 for direct use or ensure to_base64 is imported

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

from config import Config
from app.models.database import get_db_connection
from app.models.user_model import find_user_by_email
from app.users.authentication.validators.email_validator import validar_email

# Assuming your to_base64 function is available,
# if it's in a separate utility file, import it:
# from app.utils.your_crypto_utils_file import to_base64

# If you don't have a shared `to_base64` and want to define it here for now:
def to_base64(data):
    if data is None:
        return None
    # Ensure data is bytes before encoding
    if isinstance(data, str): # Handle cases where it might still be a string (e.g., old DB entries)
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


login_blueprint = Blueprint('login', __name__)
SECRET_KEY = os.environ.get("SECRET_KEY")

@login_blueprint.route('', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    # Se quiser colocar para veficar o email de forma segura.
    # validacao = validar_email(email)
    # if not validacao['valid']:
    #   return jsonify({
    #     "erro": "E-mail inválido",
    #     "detalhes": validacao['reason'],
    #     "confiabilidade": validacao['confidence']
    #   }), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone, senha, userUUID, bio, pic, public_key FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        senha_hash = usuario["senha"]
        if isinstance(senha_hash, str):
            senha_hash = senha_hash.encode('utf-8')

        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            # Convert public_key bytes to Base64 string before adding to payload
            public_key_for_jwt = None
            if usuario["public_key"]: # Check if public_key exists
                # public_key_for_jwt = to_base64(usuario["public_key"]) # Convert to Base64
                public_key_for_jwt = usuario["public_key"] # Convert to Base64
                # print(sasaspublic_key_for_jwt)

            payload = {
                'user_id': usuario["id"],
                'nome': usuario["nome"],
                'email': usuario["email"],
                'bio': usuario["bio"],
                'telefone': usuario["telefone"],
                'userUUID': usuario["userUUID"],
                'pic': usuario["pic"],
                'public_key': public_key_for_jwt, # <-- NOW IT'S BASE64 STRING!
                'exp': datetime.utcnow() + timedelta(days=365) # Consider a shorter expiration for security
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({
                "mensagem": "Login realizado com sucesso!",
                "token": token
            })

    return jsonify({"erro": "Email ou senha incorretos!"}), 401