from flask import Blueprint, request, jsonify
from app.services.email_service import enviar_email
from app.models.database import get_db_connection
import random, string

recovery_blueprint = Blueprint('recovery', __name__)

@recovery_blueprint.route('', methods=['POST'])
def solicitar_recuperacao():
    email = request.json.get('email')
    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Conectar ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Primeiro deleta códigos existentes para este email
        cursor.execute("DELETE FROM recoverCodes WHERE email = ?", (email,))
        
        # Insere o novo código
        cursor.execute("INSERT INTO recoverCodes(email, code) VALUES (?, ?)", (email, codigo))
        conn.commit()
        
        enviar_email(email, codigo)
        return jsonify({"mensagem": "Código enviado!"})
        
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"erro": "Erro inesperado!"}), 500
        
    finally:
        conn.close()