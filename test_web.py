import unittest
import websocket
import json

class WebSocketConnectionTestCase(unittest.TestCase):
    def test_websocket_connection(self):
        # Define the WebSocket server URL
        server_url = "ws://127.0.0.1:5000"  # Replace with your server's WebSocket URL

        player_id = "unique_player_id"  # Replace with the actual player ID
        game_id = "unique_game_id"  # Replace with the actual game ID

        # Attempt to establish a connection to the WebSocket server
        try:
            ws = websocket.create_connection(server_url)

            # Send a message with player and game IDs to join a game
            join_message = {
                'player_id': player_id,
                'game_id': game_id
            }
            ws.send(json.dumps(join_message))

            # Close the connection if it was successfully established
            ws.close()
        except Exception as e:
            self.fail(f"WebSocket connection failed: {e}")

if __name__ == "__main__":
    unittest.main()
