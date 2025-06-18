from flask import Blueprint

groups_blueprint = Blueprint('groups', __name__)

# Importe todas as rotas depois de criar o blueprint
from . import add_members
from . import create_group
from . import get_roomcode
from . import list_message
