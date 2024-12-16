import sqlite3

def criar_tabela_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Criar a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    print("Tabela de usuários criada com sucesso!")

# Chama a função para criar a tabela ao iniciar o app
criar_tabela_usuarios()
