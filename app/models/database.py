import sqlite3
from flask import current_app

def get_db_connection():
    """Conecta ao banco de dados."""
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados."""
    conn = get_db_connection()
    with open('database/schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()  # Certifique-se de confirmar as mudanças no banco de dados
    conn.close()
