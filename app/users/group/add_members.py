import re
import uuid

from flask import Blueprint, jsonify, request

from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/add/member', methods=['POST'])
@token_required
def add_members():
    data = request.json
    userUUID = data.get('userUUID')
    numeroDoAmigo = data.get('numero')
    group_uuid = data.get('group_uuid')

    if not all([userUUID, numeroDoAmigo, group_uuid]):
        return jsonify({'success': False, 'error': 'Dados incompletos'})

    con = get_db_connection()
    cur = con.cursor()

    # Verifica se o número do amigo existe
    cur.execute("SELECT id FROM usuarios WHERE telefone = ?", (numeroDoAmigo,))
    amigo = cur.fetchone()

    if not amigo:
        con.close()
        return jsonify({'success': False, 'error': 'Contato não encontrado'})

    amigo_id = amigo['id']

    # Obtém o group_id usando o UUID do grupo
    cur.execute("SELECT id FROM groups WHERE uuid = ?", (group_uuid,))
    group_info = cur.fetchone()

    if not group_info:
        con.close()
        return jsonify({'success': False, 'error': 'Grupo não encontrado'})

    group_id = group_info['id']

    # Verifica se o amigo já está no grupo
    cur.execute("SELECT 1 FROM group_members WHERE group_id = ? AND user_id = ?", (group_id, amigo_id))
    if cur.fetchone():
        con.close()
        return jsonify({'success': False, 'error': 'Usuário já está no grupo'})

    # Adiciona o amigo ao grupo
    cur.execute(
        "INSERT INTO group_members (user_id, group_id, group_uuid) VALUES (?, ?, ?)",
        (amigo_id, group_id, group_uuid)
    )

    con.commit()
    con.close()

    return jsonify({'success': True})
