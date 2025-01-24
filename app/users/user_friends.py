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
        SELECT 
            f.id AS friendship_id,
            u1.id AS user_id,
            u1.nome AS user_name,
            u2.id AS friend_id,
            u2.nome AS friend_name
        FROM 
            friendships f
        JOIN 
            usuarios u1 ON f.user_id = u1.id
        JOIN 
            usuarios u2 ON f.friend_id = u2.id
        WHERE 
            f.user_id = ?; -- Substitua o ? pelo ID do usuário desejado
    ''', (user_id,))

    amigos = cursor.fetchall()
    conn.close()

    # Formata os resultados para retornar como JSON
    resultado = [{"id": amigo["id"], "nome": amigo["nome"], "email": amigo["email"]} for amigo in amigos]
    return jsonify(resultado)

@friends_blueprint.route('/add', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def addFriends():
    return jsonify({"For what": "To add a new friend!"}), 200

@friends_blueprint.route('/LA', methods=['GET'])
# @verificar_token  # Protege este endpoint com verificação de token
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email FROM usuarios')  # Apenas ID, nome e e-mail
    usuarios = cursor.fetchall()
    conn.close()

    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)

