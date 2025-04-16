from app import create_app
from app.websocket import socketio 

app = create_app()

if __name__ == '__main__':

    # Correto! no caso a porta 5001. OBS: não precisa tirar o debug depois.
    socketio.run(app, debug=True, host="127.0.0.1", port=5001)
