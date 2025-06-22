import sqlite3
import base64

def is_base64_valid(s):
    """
    Verifica se uma string é uma Base64 válida.
    """
    if not isinstance(s, str):
        return False, "Não é uma string"
    # Base64 strings devem ter um comprimento múltiplo de 4
    if len(s) % 4 != 0:
        return False, "Comprimento inválido (não é múltiplo de 4)"
    try:
        # Tenta decodificar a string Base64
        base64.b64decode(s, validate=True)
        return True, "Base64 válida"
    except Exception as e:
        return False, f"Erro de decodificação Base64: {e}"

def check_user_public_keys(db_path="seu_banco_de_dados.db"):
    """
    Conecta-se ao banco de dados SQLite e verifica a validade Base64
    das chaves públicas dos usuários.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, public_key FROM usuarios")
        users = cursor.fetchall()

        if not users:
            print("Nenhum usuário encontrado na tabela 'usuarios'.")
            return

        print(f"\n--- Verificando chaves públicas no banco de dados: {db_path} ---")
        for user in users:
            user_id = user["id"]
            user_name = user["nome"]
            public_key = user["public_key"]

            print(f"\nUsuário ID: {user_id}, Nome: {user_name}")
            print(f"Chave pública armazenada (raw): '{public_key}'")

            valid, reason = is_base64_valid(public_key)
            if valid:
                print(f"Status: ✅ {reason}")
            else:
                print(f"Status: ❌ {reason}")
                print("  => Esta chave provavelmente não está em um formato Base64 adequado.")
                print("  => Se a chave acima parece estranha, o problema está na gravação no DB.")
                print("  => Se a chave estiver vazia, certifique-se de que ela está sendo enviada e salva.")


    except sqlite3.Error as e:
        print(f"Erro ao conectar ou consultar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Substitua 'seu_banco_de_dados.db' pelo caminho real do seu arquivo .db
    check_user_public_keys("/var/www/html/Radiogram.api/database/database.db")