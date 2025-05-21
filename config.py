import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o arquivo .env

class Config:
    DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')
    SECRET_KEY = os.getenv('SECRET_KEY')
    # MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2 GB

# print(f"SECRET_KEY carregada: {repr(Config.SECRET_KEY)}")
