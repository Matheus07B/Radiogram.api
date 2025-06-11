import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o arquivo .env

class Config:
  DATABASE = os.path.join(os.getcwd(), 'database', 'database.db')
  SECRET_KEY = os.getenv('SECRET_KEY')

  EMAIL_SENDER = os.getenv('EMAIL_SENDER')
  EMAIL_KEY = os.getenv('EMAIL_KEY')

  BLOCKED_EMAIL_DOMAINS = os.getenv('BLOCKED_EMAIL_DOMAINS')
  ALLOWED_TLDS = os.getenv('ALLOWED_TLDS')
  SMTP_TIMEOUT = os.getenv('SMTP_TIMEOUT')
  HELO_DOMAIN = os.getenv('HELO_DOMAIN')
  TEST_EMAIL = os.getenv('TEST_EMAIL')
  UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
  STORAGE_API_URL = os.getenv('STORAGE_API_URL')
  
  # MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')

# print(f"SECRET_KEY carregada: {repr(Config.SECRET_KEY)}")
