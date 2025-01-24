import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
import sqlite3
import bcrypt
from datetime import datetime, timedelta
import jwt  # Importando o JWT
from functools import wraps

# Configurações de chave secreta para JWT
SECRET_KEY = '8d8f3a2b84c56b7d6d981234b029dd7c183b592dc76849241afc2688a59d8be7'

# Flask e CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar a tabela de códigos de recuperação
def criar_tabela_codigos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS codigos_recuperacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        codigo TEXT NOT NULL,
        expirado INTEGER NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

criar_tabela_codigos()

@app.route('/')
def home():
    return jsonify({"message": "API funcionando corretamente!"})

# Função para verificar o token JWT em endpoints protegidos
def verificar_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401

        try:
            token = token.split()[1]  # Remove 'Bearer' do token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']  # Adiciona o user_id à requisição
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return func(*args, **kwargs)
    return decorator

# Endpoint de cadastro de usuários
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')

    if not nome or not senha or not email:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

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


# Endpoint de login com verificação de senha criptografada e geração de token JWT
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
        # Gerar o token JWT
        payload = {
            'user_id': usuario["id"],
            'email': usuario["email"],
            'exp': datetime.utcnow() + timedelta(hours=1)  # Expira em 1 hora
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"mensagem": "Login realizado com sucesso!", "token": token})
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401


# Endpoint para listar usuários (apenas com autenticação)
@app.route('/listar-usuarios', methods=['GET'])
@verificar_token  # Protege este endpoint com verificação de token
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email FROM usuarios')  # Apenas ID, nome e e-mail
    usuarios = cursor.fetchall()
    conn.close()

    resultado = [{"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]} for usuario in usuarios]
    return jsonify(resultado)


# Endpoint para solicitar recuperação de senha (envio de código)
@app.route('/solicitar-recuperacao', methods=['POST'])
# @verificar_token  # Protege este endpoint com verificação de token
def solicitar_recuperacao():
    dados = request.json
    email = dados.get('email')

    if not email:
        return jsonify({"erro": "E-mail é obrigatório"}), 400

    # Gerar código aleatório de 6 dígitos
    codigo = ''.join(random.choices(string.digits, k=6))

    # Definir tempo de expiração (10 minutos)
    expiracao = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

    # Salvar código no banco
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO codigos_recuperacao (email, codigo, expirado)
        VALUES (?, ?, 0)
    ''', (email, codigo))
    conn.commit()
    conn.close()

    # Enviar o código por e-mail
    enviar_email(email, codigo)

    return jsonify({"mensagem": "Código enviado para seu e-mail!"}), 200


def enviar_email(email_destinatario, codigo):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_sender = "matheusveneski654@gmail.com"
    email_password = "tfaz ovlq rgnb sskq"

    subject = "Código de Recuperação"
    body = f"Seu código de recuperação é: {codigo}"

    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_destinatario
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_destinatario, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


# Endpoint para validar o código de recuperação
@app.route('/validar-codigo', methods=['POST'])
def validar_codigo():
    dados = request.json
    email = dados.get('email')
    codigo = dados.get('codigo')

    if not email or not codigo:
        return jsonify({"erro": "E-mail e código são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM codigos_recuperacao WHERE email = ? AND codigo = ? AND expirado = 0
    ''', (email, codigo))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return jsonify({"erro": "Código inválido ou expirado"}), 400

    data_criacao = datetime.strptime(resultado['data_criacao'], '%Y-%m-%d %H:%M:%S')
    if datetime.now() > data_criacao + timedelta(minutes=10):
        cursor.execute('UPDATE codigos_recuperacao SET expirado = 1 WHERE id = ?', (resultado['id'],))
        conn.commit()
        conn.close()
        return jsonify({"erro": "Código expirado"}), 400

    conn.close()
    return jsonify({"mensagem": "Código validado com sucesso!"}), 200


# Endpoint para alterar a senha do usuário
@app.route('/alterar-senha', methods=['POST'])
def alterar_senha():
    dados = request.json
    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({"erro": "E-mail e nova senha são obrigatórios"}), 400

    senha_criptografada = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios SET senha = ? WHERE email = ?
    ''', (senha_criptografada, email))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Senha alterada com sucesso!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
