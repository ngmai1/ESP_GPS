import socketio
import eventlet
from flask import Flask,request

# Create a Flask app
app = Flask(__name__)

# Create a Socket.IO server
sio = socketio.Server()

# Attach the Socket.IO server to the Flask app
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Define a route for the Flask app
@app.route('/')
def index():
    return "Socket.IO server is running!"


# Define a route for the POST endpoint
@app.route('/esp32', methods=['POST'])
def esp32():
    # Get the posted data
    data = request.get_json()  # Assuming the client sends JSON data
    print('Data received from client:', data)
    return 'Data received!', 200

# Define an event handler for the 'connect' event
@sio.event
def connect(sid, environ):
    print('Connect event triggered')
    print('Client connected:', sid)
    sio.emit('message_esp32', 'Welcome!')

# Define an event handler for the 'disconnect' event
@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# Define an event handler for a custom event
@sio.event
def message(sid, data):
    print('Message from', sid, ':', data)
    sio.emit('message', 'Message received!', room=sid)

# Define an event handler for a custom event
@sio.event
def message_esp32(sid, data):
    print('Message from', sid, ':', data)
    sio.emit('message_esp32', 'Message received!')

# Run the server
if __name__ == '__main__':
    print('Starting server...')
    eventlet.wsgi.server(eventlet.listen(('192.168.8.250', 3000)), app)
    app.run(host='192.168.8.250', port=3000)
