from flask import request, jsonify
from functools import wraps
from app.services.jwt_service import decode_token

def verificar_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401

        try:
            token = token.split()[1]  # Remove 'Bearer' do token
            payload = decode_token(token)
            request.user_id = payload['user_id']
        except Exception:
            return jsonify({"erro": "Token inválido ou expirado"}), 401

        return func(*args, **kwargs)
    return decorator
