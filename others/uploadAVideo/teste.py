# import requests

# # Caminho do arquivo
# file_path = "/mnt/c/Users/mathe/Downloads/videoplayback.mp4"

# # URL da sua API (substitua pela real)
# url = "https://cloud-personal.onrender.com/upload"

# # Abre o arquivo em modo binário e envia via POST
# with open(file_path, 'rb') as file:
#     files = {'file': (file_path.split("\\")[-1], file, 'video/mp4')}
#     response = requests.post(url, files=files)

# # Exibe a resposta da API
# print("Status:", response.status_code)
# print("Resposta:", response.text)

# Base64 ====

import base64
import requests
import os

# Caminho do arquivo
file_path = "/mnt/c/Users/mathe/Downloads/videoplayback.mp4"

# URL da sua API
url = "https://cloud-personal.onrender.com/upload"

# Lê o arquivo e converte para base64
with open(file_path, 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')

# Monta o payload JSON
payload = {
    "filename": os.path.basename(file_path),
    "filedata": encoded_string,
    "mimetype": "video/mp4"
}

# Envia como JSON
response = requests.post(url, json=payload)

# Exibe a resposta
print("Status:", response.status_code)
print("Resposta:", response.text)
