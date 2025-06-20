import uuid

from flask import Blueprint, jsonify, request

from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/create', methods=['POST'])
def create_group():
    data = request.json
    name = data.get('name')               # Nome do grupo
    user_id = data.get('user_id')         # ID numérico do usuário (para group_members)
    nome = data.get('nome')               # UUID ou nome do criador (para creator_uuid)
    description = data.get('description') # Descrição opcional
    image_url = data.get('image_url')     # URL da imagem opcional

    if not name or not user_id or not nome:
        return jsonify({
            'success': False,
            'error': 'Nome do grupo, user_id e nome do criador são obrigatórios.'
        }), 400

    con = get_db_connection()
    cur = con.cursor()

    group_uuid = str(uuid.uuid4())

    # Montagem dinâmica da query
    columns = ['name', 'uuid', 'creator_name']
    values = [name, group_uuid, nome]

    if description:
        columns.append('description')
        values.append(description)
    if image_url:
        columns.append('image_url')
        values.append(image_url)

    query = f"INSERT INTO groups ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})"
    cur.execute(query, values)
    group_id = cur.lastrowid

    # Adiciona o criador como membro
    cur.execute("INSERT INTO group_members (user_id, group_id) VALUES (?, ?)", (user_id, group_id))

    con.commit()
    con.close()

    return jsonify({
        'success': True,
        'group_uuid': group_uuid
    }), 201
