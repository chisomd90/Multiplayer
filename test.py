import unittest
import eventlet
import logging
from app import app, socketio  # Import your Flask app and socketio instance

def setUpModule():
    global app_client, server_thread, client
    app_client = app.test_client()
    app_client.testing = True
    server_thread = eventlet.spawn(socketio.run, app, host='localhost', port=5000)
    client = socketio.Client()
    client.connect('http://localhost:5000')
    client.sleep(1)

def tearDownModule():
    client.disconnect()
    server_thread.kill()

def test_index_page():
    response = app_client.get('/')
    assert response.status_code == 200

def test_join_game():
    client.emit('join', {'player_id': 'PlayerA', 'game_id': 'Game1'})
    response = client.get_received()
    message_event = next(event for event in response if event['name'] == 'message')
    assert 'Player PlayerA has joined the game.' in message_event['args'][0]

def test_move():
    # Simulate a player's movement and test game updates
    pass

def test_example(self):
    logging.info("This is an informational message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")


if __name__ == '__main__':
    unittest.main()
