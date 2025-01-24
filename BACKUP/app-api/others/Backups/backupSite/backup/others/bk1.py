from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Função para login (verifica nome e senha)
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')

    if not nome or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (nome, senha))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({"mensagem": "Login realizado com sucesso!", "usuario": {"id": usuario[0], "nome": usuario[1]}})
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True)
