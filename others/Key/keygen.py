# =============================================== #
#
#  Esse código é unicamente para gerar uma 
#  Secret Key caso necessário.
#  Ele não interfere no uso da API.
#
# =============================================== #

import secrets

secret_key = secrets.token_urlsafe(256)
print(secret_key)     
