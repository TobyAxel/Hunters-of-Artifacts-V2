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
    if game == None:
        return jsonify({'message': 'No such game'}), 404
    
    # return game if found
    return jsonify(game), 200



# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)