from app.models.database import get_db_connection

def find_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(nome, email, senha_criptografada):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
        (nome, email, senha_criptografada)
    )
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, senha FROM usuarios')
    users = cursor.fetchall()
    conn.close()
    return users
