import unittest
import coverage

cov = coverage.coverage()
cov.start()

from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
disconnected = None


@socketio.on('connect')
def on_connect():
    send('connected')

 
@socketio.on('disconnect')
def on_disconnect():
    global disconnected
    disconnected = '/'


@socketio.on('connect', namespace='/test')
def on_connect_test():
    send('connected-test')


@socketio.on('disconnect', namespace='/test')
def on_disconnect_test():
    global disconnected
    disconnected = '/test'


@socketio.on('message')
def on_message(message):
    send(message)
    if message == 'test session':
        session['a'] = 'b'
    if message not in "test noack":
        return message

@socketio.on('broadcast_event')
def on_custom_event_broadcast(data):
    emit('my custom response', data, broadcast=True)


def len_150(message):
    if len(message) > 150:
        message = message[:150]
    return message

def len_50(message):
    if len(message) > 50:
        message = message[:50]
    return message


@socketio.on('join room')
def on_join_room(data):
   join_room(data['room'])


@socketio.on('leave room')
def on_leave_room(data):
    leave_room(data['room'])


@socketio.on('join room', namespace='/test')
def on_join_room_namespace(data):
    join_room(data['room'])


@socketio.on('leave room', namespace='/test')
def on_leave_room_namespace(data):
    leave_room(data['room'])


@socketio.on('my room event')
def on_room_event(data):
    room = data.pop('room')
    emit('my room response', data, room=room)


class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):
        client = socketio.test_client(app)
        received = client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'connected')
        client.disconnect()

    def test_connect_namespace(self):
        client = socketio.test_client(app, namespace='/test')
        received = client.get_received('/test')
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'connected-test')
        client.disconnect(namespace='/test')

    def test_disconnect(self):
        global disconnected
        disconnected = None
        client = socketio.test_client(app)
        client.disconnect()
        self.assertEqual(disconnected, '/')

    def test_send(self):
        client = socketio.test_client(app)
        client.get_received()
        client.send('echo this message back')
        received = client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'echo this message back')

    def test_broadcast(self):
        #message more than 150 chars 
        message_big='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
            'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'\
            'CCCCCCCCCCCCCCCCC'
        #message 150 chars
        message_150='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
            'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'


        message_big = len_150(message_big)
        client1 = socketio.test_client(app)
        client2 = socketio.test_client(app)
        client3 = socketio.test_client(app, namespace='/test')
        client2.get_received()
        client3.get_received('/test')
        client1.emit('broadcast_event', {'a': 'b'}, broadcast=True)
        client1.emit('broadcast_event', {'long_message': message_big}, broadcast=True)

        received = client2.get_received()
        self.assertEqual(len(received), 2)
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'my custom response')
        self.assertEqual(received[0]['args'][0]['a'], 'b')
        self.assertEqual(received[1]['args'][0]['long_message'], message_150)
        self.assertEqual(len(client3.get_received('/test')), 0)

    def test_room(self):
        client1 = socketio.test_client(app)
        client2 = socketio.test_client(app)
        client3 = socketio.test_client(app, namespace='/test')
        client1.get_received()
        client2.get_received()
        client3.get_received('/test')
        #Long name of room
        room_big='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \
            'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
        room_big = len_50(room_big)
        #message 50 chars
        client1.emit('join room', {'room': 'one'})
        client1.emit('join room', {'room': room_big})
        
        client2.emit('join room', {'room': 'one'})
        client2.emit('join room', {'room': room_big})
        
        client3.emit('join room', {'room': 'one'}, namespace='/test')
        client3.emit('join room', {'room': room_big}, namespace='/test')
        
        client1.emit('my room event', {'a': 'b', 'room': room_big})
        received = client1.get_received()
        
        self.assertEqual(len(received), 1)
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'my room response')
        self.assertEqual(received[0]['args'][0]['a'], 'b')
        self.assertEqual(received, client2.get_received())
        
        received = client3.get_received('/test')
        self.assertEqual(len(received), 0)
        client1.emit('leave room', {'room': room_big})
        client1.emit('my room event', {'a': 'b', 'room': room_big})
        received = client1.get_received()
        self.assertEqual(len(received), 0)

        received = client2.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'my room response')
        self.assertEqual(received[0]['args'][0]['a'], 'b')
        client2.disconnect()
        socketio.emit('my room event', {'a': 'b'}, room=room_big)
        received = client1.get_received()
        self.assertEqual(len(received), 0)

if __name__ == '__main__':
    unittest.main()
