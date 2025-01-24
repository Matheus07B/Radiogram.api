from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)

# Configuração da sessão
app.config['SECRET_KEY'] = 'chave_secreta'  # Use uma chave forte
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Simulação de banco de dados
usuarios = {
    "usuario1": "senha123",
    "usuario2": "minhasenha",
}

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario = dados.get('usuario')
    senha = dados.get('senha')

    if usuario in usuarios and usuarios[usuario] == senha:
        session['usuario'] = usuario  # Salva o usuário na sessão
        return jsonify({"mensagem": "Login realizado com sucesso!", "redirect": "/menu"}), 200
    else:
        return jsonify({"mensagem": "Usuário ou senha incorretos!"}), 401

# Rota do menu inicial
@app.route('/menu', methods=['GET'])
def menu():
    if 'usuario' in session:  # Verifica se o usuário está autenticado
        return jsonify({"mensagem": f"Bem-vindo ao menu inicial, {session['usuario']}!"}), 200
    else:
        # Redireciona para a página de login se não estiver autenticado
        return jsonify({"mensagem": "Acesso negado! Faça login para continuar.", "redirect": "/login"}), 401

if __name__ == '__main__':
    app.run(debug=True)
