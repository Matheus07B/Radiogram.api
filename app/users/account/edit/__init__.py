from flask import Blueprint

edit_blueprint = Blueprint('edit', __name__)

# Importe todas as rotas depois de criar o blueprint
from . import information
from . import pic

# Adicione mais imports para outros arquivos de rotas aqui