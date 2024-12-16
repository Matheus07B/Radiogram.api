from flask import Flask, request, jsonify, session
from flask_session import Session

app = Flask(__name__)

# Configuração da sessão
app.config['SECRET_KEY'] = 'chave_secreta'  # Use uma chave forte e secreta
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
        return jsonify({"mensagem": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Usuário ou senha incorretos!"}), 401

# Rota protegida
@app.route('/pagina-protegida', methods=['GET'])
def pagina_protegida():
    if 'usuario' in session:  # Verifica se o usuário está autenticado
        return jsonify({"mensagem": f"Bem-vindo, {session['usuario']}! Esta é uma página protegida."}), 200
    else:
        return jsonify({"mensagem": "Acesso negado! Faça login para acessar esta página."}), 401

# Rota de logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return jsonify({"mensagem": "Logout realizado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
