from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store game information
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    player_id = data['player_id']
    game_id = data['game_id']

    # Handle errors related to joining
    if game_id not in games:
        emit('error', 'Game not found', room=request.sid)
        return

    if player_id in games[game_id]['players']:
        emit('error', 'Player ID already in use', room=request.sid)
        return

    join_room(game_id)
    games[game_id]['players'][player_id] = {'socket': request.sid}
    emit('message', f'Player {player_id} has joined the game.', room=game_id)

@socketio.on('move')
def handle_move(data):
    player_id = data['player_id']
    game_id = data['game_id']
    move_data = data['move_data']

    # Handle errors related to moves
    if game_id not in games:
        emit('error', 'Game not found', room=request.sid)
        return

    if player_id not in games[game_id]['players']:
        emit('error', 'Player not found in the game', room=request.sid)
        return

    # Update game state and data based on the move_data
    # You should implement your game logic here

    # Broadcast the updated data to all players in the game
    emit('game_update', {'game_data': games[game_id]['game_data']}, room=game_id)

@socketio.on('disconnect')
def handle_disconnect():
    for game_id, game_data in games.items():
        players = game_data['players']
        for player_id, player_info in players.copy().items():
            if player_info['socket'] == request.sid:
                del players[player_id]
                emit('message', f'Player {player_id} has left the game.', room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
