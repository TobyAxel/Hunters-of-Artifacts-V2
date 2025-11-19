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
        return jsonify({'message': 'No such game'}), 404
    
    # return game if found
    return jsonify(game), 200

# Endpoint to create a new game
@app.route('/games', methods=['POST'])
def create_game():
    # check if request is json
    if request.is_json == False:
        return jsonify({'error': 'Request must be JSON'}), 400

    # get json data, validate required fields
    data = request.get_json()
    if data.get('round') is None or data.get('max_round') is None or data.get('modifier') is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # try to create game
    try:
        new_game_id = create_new_game(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # return success message
    return jsonify({'message': 'Game created', 'game_id': new_game_id}), 201

# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)