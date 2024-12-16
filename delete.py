import sqlite3
import os

# Caminho absoluto do banco de dados
db_name = os.path.expanduser("/data/data/com.termux/files/home/message-api/database.db")

# Função para deletar todos os registros da tabela
def delete_expired_codes():
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Query para deletar todos os registros
        query = "DELETE FROM codigos_recuperacao"
        cursor.execute(query)
        conn.commit()

        print(f"[DEBUG] Todos os registros da tabela 'codigos_recuperacao' foram excluídos com sucesso.")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao deletar registros: {e}")
    finally:
        if conn:
            conn.close()

# Executa a função uma única vez
delete_expired_codes()
