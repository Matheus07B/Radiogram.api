import sqlite3
from flask import current_app

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with current_app.app_context():
        conn = get_db_connection()
        with open('database/schema.sql') as f:
            conn.executescript(f.read())
        conn.close()
