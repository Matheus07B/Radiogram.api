# from app.services.jwt_service import decode_token
from flask import request, jsonify
from functools import wraps
import jwt  # Certifique-se de importar o PyJWT
from config import Config  # Importe as configurações

def verificar_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401

        try:
            token = token.split()[1]  # Remove 'Bearer' do token
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']  # Adiciona o user_id à requisição
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return func(*args, **kwargs)
    return decorator
