from flask import jsonify

# =============================================
#               IMPORTAÇÕES
# =============================================

# Rotas de conexão e utilitários
from app.ping.connection import connection_blueprint
from app.ping.helloworld import helloworld_blueprint
from app.ping.email import email_blueprint

# Autenticação de usuário
from app.users.authentication.user_login import login_blueprint
from app.users.authentication.user_register import register_blueprint

# Gerenciamento de usuário
from app.users.friends import friends_blueprint
from app.users.group import groups_blueprint

# Gerenciamento de conta
from app.users.account.edit import edit_blueprint
from app.users.account.recovery_account import recovery_blueprint
from app.users.account.verify_code import verify_recover_code_blueprint
from app.users.account.change_password import change_password_blueprint

# Comunicação em tempo real
from app.websocket.websocket_chat import websocket_blueprint
from app.users.chat.chat_options import chat_blueprint

# Serviços
from app.services.upload.upload_service import upload_blueprint

# =============================================
#          REGISTRO DAS ROTAS
# =============================================

def register_routes(app):
    # Rotas básicas de conexão e teste
    app.register_blueprint(email_blueprint, url_prefix='/email')
    app.register_blueprint(helloworld_blueprint, url_prefix='/helloworld')
    app.register_blueprint(connection_blueprint, url_prefix='/connection')

    # Rotas de autenticação
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(register_blueprint, url_prefix='/register')

    # Rotas de relacionamentos
    app.register_blueprint(friends_blueprint, url_prefix='/friends')
    app.register_blueprint(groups_blueprint, url_prefix='/groups')

    # Rotas de gerenciamento de conta
    app.register_blueprint(edit_blueprint, url_prefix='/edit')
    app.register_blueprint(recovery_blueprint, url_prefix='/recovery')
    app.register_blueprint(verify_recover_code_blueprint, url_prefix='/verifycode')
    app.register_blueprint(change_password_blueprint, url_prefix='/changepassword')

    # Rotas de comunicação
    app.register_blueprint(websocket_blueprint, url_prefix='/websocket')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    # Rotas de serviços
    app.register_blueprint(upload_blueprint, url_prefix='/upload')