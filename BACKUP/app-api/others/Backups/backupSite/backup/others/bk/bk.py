from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulação de banco de dados (dicionário)
usuarios = {
    "usuario1": "senha123",
    "usuario2": "minhasenha",
}

@app.route('/login', methods=['POST'])
def login():
    dados = request.json  # Recebe os dados no formato JSON
    usuario = dados.get('usuario')
    senha = dados.get('senha')

    # Verificação simples
    if usuario in usuarios and usuarios[usuario] == senha:
        return jsonify({"mensagem": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"mensagem": "Usuário ou senha incorretos!"}), 401

if __name__ == '__main__':
    app.run(debug=True)

