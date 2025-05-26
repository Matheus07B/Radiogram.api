from flask import Blueprint, request, jsonify
from app.services.email_service import enviar_email
from app.models.database import get_db_connection
import random, string
import sqlite3

recovery_blueprint = Blueprint('recovery', __name__)

@recovery_blueprint.route('', methods=['POST'])
def solicitar_recuperacao():
    email = request.json.get('email')
    codigo = ''.join(random.choices(string.digits, k=12))

    # Conectar ao banco de dados
    cursor = get_db_connection()

    # Query de inserção
    query = "INSERT INTO recoverCodes(email, code) VALUES (?, ?)"
    data = (email, codigo)

    # Executar a query para salvar a imagem no banco de dados
    cursor.execute(query, data)
    cursor.commit()
    cursor.close()

    enviar_email(email, codigo)
    return jsonify({"mensagem": "Código enviado!"})
