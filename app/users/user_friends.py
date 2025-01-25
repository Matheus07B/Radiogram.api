from flask import Blueprint, jsonify, request
from app.models.user_model import get_all_users
from app.utils.decorators import verificar_token
from app.models.database import get_db_connection
from config import Config
import jwt

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/list', methods=['GET'])
def list_friends():
    # Obter o token do cabeçalho Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token de autorização é obrigatório"}), 401

    # Verificar se o cabeçalho está no formato esperado "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Formato de token inválido"}), 401

    try:
        # Extrair o token
        token = auth_header.split(" ")[1]
        # Decodificar o token JWT usando a SECRET_KEY da configuração
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")  # Obter o user_id do payload
        if not user_id:
            return jsonify({"error": "Token inválido: user_id não encontrado"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirou"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Consulta ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT u.id, u.nome, u.email
                      FROM friendships f
                      JOIN usuarios u ON f.friend_id = u.id
                      WHERE f.user_id = ?''', (user_id,))
    friends = cursor.fetchall()
    conn.close()

    # Formatar os resultados para retornar como JSON
    friends = [{"id": friend["id"], "nome": friend["nome"], "email": friend["email"]} for friend in friends]
    return jsonify(friends), 200


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

