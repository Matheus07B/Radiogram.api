from app import create_app

app, socketio = create_app()  # Obtém a app Flask e o WebSocket

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)

##########################################

# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
