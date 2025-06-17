from flask import Blueprint, request, jsonify
from app.models.database import get_db_connection

verify_recover_code_blueprint = Blueprint('verifycode', __name__)

@verify_recover_code_blueprint.route('', methods=['POST'])
def verificar_codigo():
    email = request.json.get('email')
    codigo = request.json.get('codigo')

    if not email or not codigo:
        return jsonify({"erro": "Email e código são obrigatórios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para verificar se o código existe para o email
        query = "SELECT * FROM recoverCodes WHERE email = ? AND code = ?"
        cursor.execute(query, (email, codigo))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            return jsonify({"mensagem": "Código verificado com sucesso!"}), 200
        else:
            return jsonify({"erro": "Código inválido ou expirado"}), 401

    except Exception as e:
        return jsonify({"erro": f"Erro interno!"}), 500
