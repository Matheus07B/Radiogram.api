import re
import jwt
import uuid
import sqlite3

from flask import Blueprint, jsonify, request

from config import Config
from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/list/select', methods=['GET'])
@token_required
def list_message():
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

    group_uuid = request.args.get('group_uuid')
    if not group_uuid:
        return jsonify({"error": "group_uuid é obrigatório"}), 400

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            SELECT 
                m.id, 
                m.message, 
                m.image, 
                m.video,
                m.document,
                m.time, 
                m.sender_id
            FROM group_messages m
            JOIN groups g ON g.id = m.group_id
            WHERE g.uuid = ?
            ORDER BY m.timestamp
            ''', (group_uuid,)
        )
        messages = cursor.fetchall()

        messages_data = []
        for message in messages:
            msg_data = {
                "id": message["id"],
                "message": message["message"],
                "time": message["time"],
                "sender_id": message["sender_id"]
            }

            if message["image"]:
                msg_data["image_url"] = message["image"]
            if message["video"]:
                msg_data["video"] = message["video"]
            if message["document"]:
                msg_data["document"] = message["document"]

            messages_data.append(msg_data)

        return jsonify({"messages": messages_data}), 200

    except Exception as e:
        print(f"Erro no banco de dados: {str(e)}")
        return jsonify({"error": "Erro interno"}), 500
    finally:
        conn.close()
