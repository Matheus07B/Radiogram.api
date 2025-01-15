from flask import Blueprint, jsonify
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['GET'])
@verificar_token
def listar_usuarios():
    users = get_all_users()
    return jsonify(users)
