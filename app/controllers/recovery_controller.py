from flask import Blueprint, request, jsonify
from app.services.email_service import enviar_email
import random, string

recovery_blueprint = Blueprint('recovery', __name__)

@recovery_blueprint.route('/solicitar', methods=['POST'])
def solicitar_recuperacao():
    email = request.json.get('email')
    codigo = ''.join(random.choices(string.digits, k=6))
    enviar_email(email, codigo)
    return jsonify({"mensagem": "Código enviado!"})
