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
    group_id = data['group_id']
    user_id = data['user_id']

    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # Verifica se já está no grupo
    cur.execute("SELECT 1 FROM group_members WHERE group_id=? AND user_id=?", (group_id, user_id))
    if cur.fetchone():
        con.close()
        return jsonify({'success': False, 'error': 'Usuário já está no grupo'})

    cur.execute("INSERT INTO group_members (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
    con.commit()
    con.close()
    return jsonify({'success': True})
