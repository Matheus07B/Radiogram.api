import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o arquivo .env

class Config:
    DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')

# print(f"SECRET_KEY carregada: {repr(Config.SECRET_KEY)}")
