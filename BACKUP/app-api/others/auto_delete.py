 import sqlite3
import time

# Nome do banco de dados
db_name = "database.db"

# Função para deletar todos os registros da tabela
def delete_expired_codes():
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Query para deletar todos os registros
        table_name = "Códigos Expirados"
        query = f"DELETE FROM codigos_recuperacao"
        cursor.execute(query)
        conn.commit()

        print(f"[DEBUG] Todos os registros da tabela 'codigos_recuperacao' foram excluídos com sucesso.")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao deletar registros: {e}")
    finally:
        if conn:
            conn.close()

# Loop infinito para executar a cada 1 minuto
while True:
    delete_expired_codes()
    time.sleep(10)  # Espera 60 segundos 6 * 5 = 360 = 5 minutos
