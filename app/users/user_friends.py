from flask import Blueprint, jsonify
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token
from app.models.database import get_db_connection

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/list', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email FROM usuarios')  # Apenas ID, nome e e-mail
    usuarios = cursor.fetchall()
    conn.close()

    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)
