from flask import Blueprint

friends_blueprint = Blueprint('friends', __name__)

# Importe todas as rotas depois de criar o blueprint
from . import add_friend
from . import delete_friend
from . import user_friends

# Adicione mais imports para outros arquivos de rotas aqui