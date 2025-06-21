import uuid

from flask import Blueprint, jsonify, request

from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import groups_blueprint

@groups_blueprint.route('/delete', methods=['POST'])
@token_required
def delete_group():
    data = request.json
    userUUID = data.get('userUUID')       # UUID do criador do grupo
    group_uuid = data.get('group_uuid')   # UUID do grupo a ser deletado

    if not all([userUUID, group_uuid]):
        return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

    con = get_db_connection()
    cur = con.cursor()

    # Busca o group_id com base no UUID
    cur.execute("SELECT id, creator_name FROM groups WHERE uuid = ?", (group_uuid,))
    group = cur.fetchone()

    if not group:
        con.close()
        return jsonify({'success': False, 'error': 'Grupo não encontrado'}), 404

    group_id = group['id']
    # creator_uuid = group['creator_name']

    # # Verifica se quem está tentando excluir é o criador (mantido comentado conforme solicitado)
    # if creator_name != userUUID:
    #     con.close()
    #     return jsonify({'success': False, 'error': 'Apenas o criador do grupo pode deletá-lo'}), 403

    # Deleta mensagens do grupo (usando group_id porque group_uuid ainda não foi adicionado à tabela)
    cur.execute("DELETE FROM group_messages WHERE group_id = ?", (group_id,))
    # cur.execute("DELETE FROM group_messages WHERE group_uuid = ?", (group_uuid,))

    # Remove todos os membros do grupo
    cur.execute("DELETE FROM group_members WHERE group_uuid = ?", (group_uuid,))

    # Deleta o próprio grupo
    cur.execute("DELETE FROM groups WHERE uuid = ?", (group_uuid,))

    con.commit()
    con.close()

    return jsonify({'success': True, 'message': 'Grupo deletado com sucesso.'})
