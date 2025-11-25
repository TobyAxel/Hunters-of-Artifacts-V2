from flask import Flask, request, jsonify
from backend_functions import *

app = Flask(__name__)

# Endpoint to fetch all games
@app.route('/games', methods=['GET'])
def fetch_games():
    # try to fetch games
    try:
        games = get_games()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # check if existing games are found
    if len(games) == 0:
        return jsonify({'message': 'No games found'}), 200

    # return games if any are found
    return jsonify(games), 200

# Endpoint to fetch a specific game by id
@app.route('/games/<int:game_id>', methods=['GET'])
def fetch_game(game_id):
    # try to fetch game
    try:
        game = get_game(game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # check if game exists
    if len(game) == 0:
        return jsonify({'message': f'No game with id {game_id} found'}), 404
    
    # return game if found
    return jsonify(game), 200

# Endpoint to check players in game
@app.route('/games/<int:game_id>/players', methods=['GET'])
def fetch_game_players(game_id):
    # fetch game
    game = fetch_game(game_id)

    # check if game exists
    if game[1] != 200:
        return game

    # get players for game
    players = get_players(game_id)

    # return players
    return players

# Endpoint to create a new game
@app.route('/games', methods=['POST'])
def create_game():
    # check if request is json
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    # get json data, validate required fields
    data = request.get_json()
    if data.get('players') is None or data.get('config') is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # try to create game
    try:
        new_game_id = create_new_game(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # return success message
    return jsonify({'message': 'Game created', 'game_id': new_game_id}), 201

#endpoint events
@app.route('/events/<int:game_id>', methods=['GET'])
def fetch_events(game_id):
    game = fetch_game(game_id)
    if game[1] != 200:
        return game

    try:
        event = get_event(game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': event}), 200

# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)