from flask import Blueprint, request, jsonify
from app.services.jwt_service import generate_token
from app.services.bcrypt_service import check_password
from app.models.user_model import find_user_by_email

auth_blueprint = Blueprint('login', __name__)

@auth_blueprint.route('/', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    user = find_user_by_email(email)
    if user and check_password(senha, user["senha"]):
        token = generate_token(user["id"], user["email"])
        return jsonify({"token": token}), 200
    return jsonify({"erro": "Credenciais inválidas"}), 401


# from flask import Blueprint, request, jsonify
# from app.services.jwt_service import generate_token
# from app.models.database import get_db_connection
# import bcrypt

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     dados = request.json
#     email = dados.get('email')
#     senha = dados.get('senha')

#     if not email or not senha:
#         return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email,))
#     usuario = cursor.fetchone()
#     conn.close()

#     if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
#         # Gerar o token JWT usando o serviço
#         token = generate_token(user_id=usuario["id"], email=usuario["email"])
#         return jsonify({"mensagem": "Login realizado com sucesso!", "token": token})
#     else:
#         return jsonify({"erro": "Credenciais inválidas"}), 401
