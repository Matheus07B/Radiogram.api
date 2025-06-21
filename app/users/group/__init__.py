from flask import Blueprint

groups_blueprint = Blueprint('groups', __name__)

# Importe todas as rotas depois de criar o blueprint
from . import create_group
from . import delete_group
from . import add_members
from . import remove_members
from . import get_roomcode
from . import list_message
