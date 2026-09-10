import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print("Client connected")

@sio.event
def message(sid, data):
    print("Message received:", data)

@sio.event
def disconnect(sid):
    print("Client disconnected")

eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)