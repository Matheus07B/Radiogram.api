import os

class Config:
    DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')  # Caminho para o banco de dados
    SECRET_KEY = '8d8f3a2b84c56b7d6d981234b029dd7c183b592dc76849241afc2688a59d8be7' # chave secreta.
