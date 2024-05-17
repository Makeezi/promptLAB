from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

messages = ['','']

@socketio.on('positive')
def handle_positive(data):
    message = "Positive message received: " + data
    print(message)
    messages[0] = data


@socketio.on('negative')
def handle_negative(data):
    message = "Negative message received: " + data
    print(message)
    messages[1] = data

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'Connected'})

@app.route('/input/<id>', methods=['GET'])
def get_input(id):
    return jsonify(messages)

if __name__ == '__main__':
    socketio.run(app, debug=True)
