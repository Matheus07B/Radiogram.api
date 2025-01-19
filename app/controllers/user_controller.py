from flask import Blueprint, jsonify
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/listar', methods=['GET'])
# @verificar_token
def listar_usuarios():
    users = get_all_users() # Lista de objetos sqlite3.Row
    users_list = [dict(row) for row in users] # Converte cada linha em um dicionário
    return jsonify({"usuarios": users_list}), 200