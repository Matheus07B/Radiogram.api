import os
import jwt
import uuid
import bcrypt
import base64 # Manter o import, pode ser útil em outras partes, mas não para salvar public_key

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

from app.models.database import get_db_connection
from app.models.user_model import find_user_by_email
from app.users.authentication.validators.email_validator import validar_email

register_blueprint = Blueprint('register', __name__)
SECRET_KEY = os.environ.get("SECRET_KEY")

@register_blueprint.route('', methods=['POST'])
def register():
    data = request.json
    nome = data.get('nome').strip()
    email = data.get('email').strip()
    telefone = data.get('concatNum').strip()
    senha = data.get('senha').strip()
    
    # PEGA A CHAVE PÚBLICA COMO STRING BASE64 DO FRONTEND
    # NÃO DECODIFIQUE AQUI! APENAS RECEBA A STRING.
    public_key_base64 = data.get("publicKeyBase64").strip() 

    if not nome or not senha or not email or not telefone or not public_key_base64:
        return jsonify({"erro": "Dados incompletos! Certifique-se de preencher todos os campos, incluindo a chave pública."}), 400

    # Removido o bloco try/except de base64.b64decode, pois não vamos decodificar antes de salvar.
    # Se você quiser validar que a string recebida é um Base64 válido,
    # pode manter um 'is_base64_valid' aqui, mas não armazene os bytes decodificados.
    # Exemplo de validação (opcional, pode ser feito no frontend ou antes de salvar):
    try:
        # Apenas para validar se é Base64 válida, NÃO para obter os bytes que serão salvos.
        base64.b64decode(public_key_base64, validate=True) 
    except Exception as e:
        print(f"Erro de validação: Chave pública Base64 recebida é inválida: {e}")
        return jsonify({"erro": "Chave pública inválida (formato Base64 inválido na chegada)."}), 400

    # Optional: Validação de e-mail (mantido comentado como no seu código)
    # validacao = validar_email(email)
    # if not validacao['valid']:
    #    return jsonify({
    #        "erro": "E-mail inválido",
    #        "detalhes": validacao['reason'],
    #        "confiabilidade": validacao['confidence']
    #    }), 400

    # Criptografa senha
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Chaves padrão (ajuste se quiser personalizar depois)
    bioENV = os.getenv("BIO_DEFAULT")
    picENV = os.getenv("IMG_DEFAULT")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se já existe nome ou email
    cursor.execute('SELECT 1 FROM usuarios WHERE nome = ? OR email = ?', (nome, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Esse nome de usuário ou email já existe!"}), 400

    user_uuid = str(uuid.uuid4())

    try:
        cursor.execute(
            '''
            INSERT INTO usuarios
            (nome, email, telefone, senha, userUUID, bio, pic, public_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            # SALVE A STRING BASE64 DIRETAMENTE AQUI!
            (nome, email, telefone, senha_criptografada, user_uuid, bioENV, picENV, public_key_base64) 
        )
        conn.commit()
    except sqlite3.Error as e: # Capture erros específicos do SQLite
        conn.rollback() # Desfaz a transação em caso de erro
        print(f"Erro ao inserir usuário no DB: {e}")
        return jsonify({"erro": "Erro ao registrar usuário no banco de dados."}), 500
    finally:
        conn.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!", "userUUID": user_uuid}), 201