from flask import Blueprint, jsonify, request
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token
from app.models.database import get_db_connection

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/list', methods=['GET'])
def list_friends():
    user_id = request.args.get('user_id')  # Obtém o ID do usuário da query string
    if not user_id:
        return jsonify({"error": "O parâmetro 'user_id' é obrigatório"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para buscar amigos do usuário
    cursor.execute('''
        SELECT u.id, u.nome, u.email
        FROM friendships f
        JOIN usuarios u ON f.friend_id = u.id
        WHERE f.user_id = ?
    ''', (user_id,))

    friend = cursor.fetchall()
    conn.close()

    # Formata os resultados para retornar como JSON
    friend = [{"id": friend["id"], "nome": friend["nome"], "email": friend["email"]} for friend in friend]
    return jsonify(friend)

@friends_blueprint.route('/add', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def addFriends():
    return jsonify({"For what": "To add a new friend!"}), 200

@friends_blueprint.route('/LA', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha FROM usuarios')  # Apenas ID, nome e e-mail
    usuarios = cursor.fetchall()
    conn.close()

    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)

