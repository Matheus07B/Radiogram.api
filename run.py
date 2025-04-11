from app import create_app
from app.websocket import socketio  # Importa socketio do websocket.py

app = create_app()

if __name__ == '__main__':
    # OBS: tirar o debug dps!
    socketio.run(app, debug=True, host="127.0.0.1", port=5001) 
