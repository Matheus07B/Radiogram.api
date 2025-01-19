# Importa a função diretamente do modulo de usuarios
# from app.models.user_model import get_all_users

from flask import jsonify

# connection routes
from app.status.connection import connection_blueprint
from app.status.helloworld import helloworld_blueprint
from app.status.email import email_blueprint

# main routes
from app.controllers.auth_controller import auth_blueprint
from app.controllers.user_controller import user_blueprint
from app.controllers.recovery_controller import recovery_blueprint

def register_routes(app):
  
    # rota main aqui
    # app.register_blueprint(main_blueprint, url_prefix='/')

    # rota de conexão aqui
    app.register_blueprint(email_blueprint, url_prefix='/email')
    app.register_blueprint(helloworld_blueprint, url_prefix='/helloworld')
    app.register_blueprint(connection_blueprint, url_prefix='/connection')

    # autenticação aqui
    app.register_blueprint(auth_blueprint, url_prefix='/login')

    # usuarios
    app.register_blueprint(user_blueprint, url_prefix='/users')

    # recuperar conta
    app.register_blueprint(recovery_blueprint, url_prefix='/recovery')

"""
    # ====== Rotas diretas ======
    #
    # @app.route('/', methods=['GET'])
    # def home():
    #     return jsonify({"message": "teste de conexão da API!"}), 200

    # @app.route('/listar', methods=['GET'])
    # def listar():
    #     users = get_all_users() # Lista de objetos sqlite3.Row
    #     users_list = [dict(row) for row in users] # Converte cada linha em um dicionário
    #     return jsonify({"usuarios": users_list}), 200
"""