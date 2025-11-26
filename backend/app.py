from flask import Flask, request, jsonify
from backend_functions import *

app = Flask(__name__)

# Endpoint to fetch all games or create a new game
@app.route('/games', methods=['GET', 'POST'])
def handle_games():
    # handle GET request to fetch all games
    if request.method == 'GET':
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
    
    # handle POST request to create a new game
    if request.method == 'POST':
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
        return jsonify({'message': 'Game created', 'games': new_game_id}), 201
    
    return jsonify({'error': 'Invalid request method'}), 405

# Endpoint to fetch a specific game by id
@app.route('/games/<int:game_id>', methods=['GET'])
def fetch_game(game_id):
    # try to fetch game
    try:
        game = get_games(game_id)
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
    return players, 200

# Endpoint to get / create event or update event state
@app.route('/events/<int:game_id>', methods=['GET', 'POST'])
def handle_events(game_id):
    # try to fetch game
    game = fetch_game(game_id)
    if game[1] != 200:
        return game

    # handle GET Request to get / create event
    if request.method == 'GET':
        # try to fetch event state
        try:
            event = get_event(game_id)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # return event state
        return jsonify({'event': event}), 200

    # Handle POST request to update event state
    if request.method == 'POST':
        # check if request is json
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        # get json data, validate required field
        data = request.get_json()
        if data.get('event_option') is None:
            return jsonify({'error': 'Missing required fields'}), 400

        # try to update game state
        try:
            new_event_state = update_event(data, game_id)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({'event': new_event_state}), 200

    return jsonify({'error': 'Invalid request method'}), 405

# Endpoint to get shop items
@app.route('/shop/<int:game_id>', methods=['GET'])
def fetch_shop(game_id):
    # try to fetch game
    try:
        game = get_games(game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # check if game exists
    if len(game) == 0:
        return jsonify({'message': f'No game with id {game_id} found'}), 404

    # Check if shop is opened
    if game[0]['max_round'] / 2 > game[0]['round']:
        return jsonify({'message': f'Shop is not opened yet.'}), 200

    try:
        shop_items = get_shop_items()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'shop': shop_items}), 200

# Endpoint to end player's turn
@app.route('/games/<int:game_id>/end-turn', methods=['POST'])
def end_player_turn(game_id):
    # try to end turn
    try:
        result = end_turn(game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # return new game state
    return jsonify(result), 200

# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)