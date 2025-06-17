import os
import re
import jwt
import bcrypt

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

from config import Config
from app.models.database import get_db_connection
from app.models.user_model import find_user_by_email
from app.users.authentication.validators.email_validator import validar_email

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
    cursor.execute('SELECT id, nome, email, telefone, senha, userUUID, bio, pic FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    
    # Verificação de senha com Hash - só descomentar se quiser usar.
    if usuario:
      senha_hash = usuario["senha"]
      if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode('utf-8')

      if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
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
          "mensagem": "Login realizado com sucesso!",
          "token": token
        })

    # ALERTA! - Apenas para testes, não rode em produção.
    # if usuario:
    #   payload = {
    #     'user_id': usuario["id"],
    #     'nome': usuario["nome"],
    #     'email': usuario["email"],
    #     'bio': usuario["bio"],
    #     'telefone': usuario["telefone"],
    #     'userUUID': usuario["userUUID"],
    #     'pic': usuario["pic"],
    #     'exp': datetime.utcnow() + timedelta(days=365)
    #   }
    #   token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    #   return jsonify({
    #     "mensagem": "Login realizado com sucesso!",
    #     "token": token
    #   })

    return jsonify({"erro": "Email ou senha incorretos!"}), 401
