# # remover caso necessario
from gevent import monkey
monkey.patch_all()
# from flask import Flask  # Agora você pode importar outras libs

from app import create_app
from app.websocket import socketio  # Importa socketio corretamente

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)  # Correto!

##########################################

# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
