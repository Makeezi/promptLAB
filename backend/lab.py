from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

messages = [["", ""]]

@socketio.on('positive')
def handle_positive(data):
    message = "Positive message received: " + data['msg']
    if(len(messages) < data['id'] + 1):
        messages.append(["", ""])
    messages[data['id']][0] = data['msg']
    print(data['msg'])



@socketio.on('negative')
def handle_negative(data):
    message = "Negative message received: " + data['msg']
    if(len(messages) < data['id'] + 1):
        messages.append(["", ""])
    messages[data['id']][1] = data['msg']
    print(data['msg'])


@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'Connected'})

@app.route('/input/<id>', methods=['GET'])
def get_input(id):
    return jsonify(messages[int(id)])

if __name__ == '__main__':
    socketio.run(app, debug=True)
