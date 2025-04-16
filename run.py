from app import create_app
from app.websocket import socketio  # Importa socketio corretamente

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1", port=5001)  # Correto! no caso a porta 5001. OBS: tirar o debug depois.
