import re
import jwt
import uuid

from flask import Blueprint, jsonify, request

from app.utils.decorators import token_required
from config import Config
from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/get/uuid', methods=['GET'])
@token_required
def get_roomcode():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token inválido ou faltando"}), 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Pega o UUID do grupo na query string
    group_uuid = request.args.get('group_uuid')
    if not group_uuid:
        return jsonify({"error": "group_uuid é obrigatório"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT uuid FROM groups WHERE uuid = ?",
        (group_uuid,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"group_uuid": result["uuid"]}), 200
    else:
        return jsonify({"error": "Grupo não encontrado"}), 404
