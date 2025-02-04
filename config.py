import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o arquivo .env

class Config:
    DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave_padrao').strip()

# print(f"SECRET_KEY carregada: {repr(Config.SECRET_KEY)}")
