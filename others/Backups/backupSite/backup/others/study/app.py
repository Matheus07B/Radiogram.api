from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'database.db'

def init_db():
    """Inicializa o banco de dados com a tabela necessária."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar o banco de dados na inicialização do app
init_db()

# Rota: Criar mensagem (POST)
@app.route('/mensagens', methods=['POST'])
def criar_mensagem():
    dados = request.json
    texto = dados.get('texto')

    if not texto:
        return jsonify({"erro": "Texto da mensagem é obrigatório"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mensagens (texto) VALUES (?)', (texto,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Mensagem criada com sucesso!"}), 201

# Rota: Ler mensagens (GET)
@app.route('/mensagens', methods=['GET'])
def listar_mensagens():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mensagens')
    mensagens = cursor.fetchall()
    conn.close()

    resultado = [{"id": msg[0], "texto": msg[1]} for msg in mensagens]
    return jsonify(resultado)

# Rota: Atualizar mensagem (PUT)
@app.route('/mensagens/<int:id>', methods=['PUT'])
def atualizar_mensagem(id):
    dados = request.json
    novo_texto = dados.get('texto')

    if not novo_texto:
        return jsonify({"erro": "Texto da mensagem é obrigatório"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE mensagens SET texto = ? WHERE id = ?', (novo_texto, id))
    conn.commit()
    atualizado = cursor.rowcount
    conn.close()

    if atualizado == 0:
        return jsonify({"erro": "Mensagem não encontrada"}), 404

    return jsonify({"mensagem": "Mensagem atualizada com sucesso!"})

# Rota: Deletar mensagem (DELETE)
@app.route('/mensagens/<int:id>', methods=['DELETE'])
def deletar_mensagem(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mensagens WHERE id = ?', (id,))
    conn.commit()
    deletado = cursor.rowcount
    conn.close()

    if deletado == 0:
        return jsonify({"erro": "Mensagem não encontrada"}), 404

    return jsonify({"mensagem": "Mensagem deletada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
