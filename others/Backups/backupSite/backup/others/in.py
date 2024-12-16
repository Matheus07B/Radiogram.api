import sqlite3

def inserir_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Inserir usuários fictícios
    usuarios = [
        ('usuario1', 'senha1'),
        ('usuario2', 'senha2'),
        ('usuario3', 'senha3'),
    ]

    cursor.executemany('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', usuarios)

    conn.commit()
    conn.close()
    print("Usuários inseridos com sucesso!")

# Chama a função para inserir usuários ao iniciar o app
inserir_usuarios()
