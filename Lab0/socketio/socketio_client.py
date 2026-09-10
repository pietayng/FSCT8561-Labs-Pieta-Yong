import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect(reason):
    print("Disconnected from server")

sio.connect("http://127.0.0.1:5000")
sio.send("Hello from client!")
sio.disconnect()