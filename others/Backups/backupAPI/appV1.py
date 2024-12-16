from flask import Flask, request, jsonify
import sqlite3  # Adicionando a importação do sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')

    if not nome or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar se o nome já existe
    cursor.execute('SELECT 1 FROM usuarios WHERE nome = ?', (nome,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Esse nome de usuário já existe!"}), 400

    try:
        cursor.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', (nome, senha))
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 201



# Endpoint para fazer consulta no banco de dados - JAVA / SITE
@app.route('/listar-usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, senha FROM usuarios')  # Apenas ID e nome (sem senha)
    usuarios = cursor.fetchall()
    conn.close()

    # Formatar os resultados como uma lista de dicionários
    resultado = [{"id": usuario[0], "nome": usuario[1], "senha": usuario[2]} for usuario in usuarios]
    return jsonify(resultado)



# Função para login (verifica nome e senha) - SITE
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
    app.run(debug=True, host='192.168.1.9', port=5000)
