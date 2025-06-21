from flask import Blueprint

connection_blueprint = Blueprint('/ping', __name__)

from . import conn
from . import email
