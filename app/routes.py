# Importa a função diretamente do modulo de usuarios
# from app.models.user_model import get_all_users
from flask import jsonify

# connection routes
from app.ping.connection import connection_blueprint
from app.ping.helloworld import helloworld_blueprint
from app.ping.email import email_blueprint

# main routes
from app.users.authentication.user_login import login_blueprint
from app.users.authentication.user_register import register_blueprint
from app.users.user_friends import friends_blueprint

from app.users.account.recovery_account import recovery_blueprint
from app.users.account.verify_code import verify_recover_code_blueprint
from app.users.account.change_password import change_password_blueprint

# websockets
from app.websocket.chat import chat_blueprint

# Upload
from app.services.upload.upload_service import upload_blueprint

# Add friend
from app.users.friends.addFriend import add_friend_blueprint

def register_routes(app):
    # rota main aqui
    # app.register_blueprint(main_blueprint, url_prefix='/')

    # rota de conexão aqui
    app.register_blueprint(email_blueprint, url_prefix='/email')
    app.register_blueprint(helloworld_blueprint, url_prefix='/helloworld')
    app.register_blueprint(connection_blueprint, url_prefix='/connection')

    # autenticação aqui
    app.register_blueprint(login_blueprint, url_prefix='/login')

    # registrar conta
    app.register_blueprint(register_blueprint, url_prefix='/register')

    # amigos
    app.register_blueprint(friends_blueprint, url_prefix='/friends')

    # recuperar conta
    app.register_blueprint(recovery_blueprint, url_prefix='/recovery')
    app.register_blueprint(verify_recover_code_blueprint, url_prefix='/verifycode')
    app.register_blueprint(change_password_blueprint, url_prefix='/changepassword')

    # Criação do websocket
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    # Upload
    app.register_blueprint(upload_blueprint, url_prefix='/upload')
    
    # Upload
    app.register_blueprint(add_friend_blueprint, url_prefix='/addfriend')
