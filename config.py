import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

class Config:
    DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')  # Caminho para o banco de dados
    SECRET_KEY = os.getenv('SECRET_KEY')  # Lê a chave secreta do .env
