import uuid

from flask import Blueprint, jsonify, request

from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/create', methods=['POST'])
def create_group():
    data = request.json
    name = data.get('name')
    user_id = data.get('user_id')

    if not name or not user_id:
        return jsonify({'success': False, 'error': 'Nome do grupo e user_id são obrigatórios'}), 400

    con = get_db_connection()
    cur = con.cursor()

    group_uuid = str(uuid.uuid4())

    # Criar o grupo com UUID
    cur.execute("INSERT INTO groups (name, uuid) VALUES (?, ?)", (name, group_uuid))
    group_id = cur.lastrowid

    # Adicionar o criador como membro
    cur.execute("INSERT INTO group_members (user_id, group_id) VALUES (?, ?)", (user_id, group_id))

    con.commit()
    con.close()

    return jsonify({
        'success': True,
        'group_uuid': group_uuid
    }), 201
