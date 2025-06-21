from flask import Blueprint

upload_blueprint = Blueprint('upload', __name__, template_folder='templates/')

# Importe todas as rotas depois de criar o blueprint
from . import upload_service

# Adicione mais imports para outros arquivos de rotas aqui