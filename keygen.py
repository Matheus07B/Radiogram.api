import secrets

secret_key = secrets.token_urlsafe(256)  # Gera uma chave segura de 64 caracteres
print(secret_key)
