from flask import Flask, request, jsonify
import sqlite3
import bcrypt
from flask_cors import CORS

# Flask para a criação da API de fato!
# Cors permite a conexão da API com qualquer porta.
# sqlite3 obviamente é o banco de dados.
# bcrypt para criptogafar as senhas, OBS: tive que baixar o rust para usar essa biblioteca.

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



# endpoint de cadastro de usuários.
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')  # Adicionando o campo email

    if not nome or not senha or not email:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Criptografar a senha
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar se o nome ou email já existem
    cursor.execute('SELECT 1 FROM usuarios WHERE nome = ? OR email = ?', (nome, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Esse nome de usuário ou email já existe!"}), 400

    try:
        cursor.execute(
            'INSERT INTO usuarios (nome, senha, email) VALUES (?, ?, ?)',
            (nome, senha_criptografada, email)
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 201



# Endpoint para listar usuários (sem retornar senhas)
@app.route('/listar-usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email FROM usuarios')  # Apenas ID, nome e email (sem senha)
    usuarios = cursor.fetchall()
    conn.close()

    # Formatar os resultados como uma lista de dicionários
    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)



# Endpoint para login com verificação de senha criptografada
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    #nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, senha FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
        return jsonify({"mensagem": "Login realizado com sucesso!", "usuario": {"id": usuario["id"], "email": usuario["email"]}})
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.9', port=5000)
