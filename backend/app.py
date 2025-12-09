from typing import Any

from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.helper_functions import is_ident
from backend_functions import *
from travel_functions import *
app = Flask(__name__)
CORS(app)

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

# Endpoint to use item
@app.route('/items/<int:game_id>', methods=['POST'])
def use_item(game_id):
    # try to fetch game
    game = fetch_game(game_id)
    if game[1] != 200:
        return game

    # check if request is json
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    # get json data, validate required field
    data = request.get_json()
    if data.get('item_name') is None:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # use item
    try: 
        result = use_player_item(data['item_name'], game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': result}), 200

# Endpoint to handle shop functions
@app.route('/shop/<int:game_id>', methods=['GET', 'POST'])
def handle_shop(game_id):
    # try to fetch game
    try:
        game = get_games(game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # check if game exists
    if len(game) == 0:
        return jsonify({'message': f'No game with id {game_id} found'}), 404

    # Get shop items
    try:
        shop_items = get_shop_items(game[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if request.method == 'GET':
        return jsonify({'shop': shop_items}), 200

    if request.method == 'POST':
        # check if request is json
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        # get json data, validate required field
        data = request.get_json()
        if data.get('item_id') is None:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            result = buy_item(data['item_id'], shop_items, game[0])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': result}), 200

    return jsonify({'error': 'Invalid request method'}), 405

# Endpoint to end player's turn
@app.route('/games/<int:game_id>/end-turn', methods=['POST'])
def end_player_turn(game_id):
    # try to end turn
    try:
        result = end_turn(game_id)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    # return new game state
    return jsonify(result), 200

# Endpoint to get a player's items
@app.route('/player/items/<int:player_id>', methods=['GET'])
def player_items(player_id):
    try:
        result = get_items(player_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

# Endpoint to get a player's active effects
@app.route('/player/active-effects/<int:player_id>', methods=['GET'])
def player_active_effects(player_id):
    try:
        result = get_active_effects(player_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

@app.route('/games/<int:game_id>/artifacts/<int:item_id>/steal', methods=['POST'])
def steal_artifacts(game_id, item_id):
    try:
        # Fetch player by the given id
        player: list[dict[Any, Any]] = get_current_player(game_id)
        # Check if user exists
        if len(player) == 0:
            return jsonify({'error': "No player with given id found"}), 404

        # Check if player has moves
        if player[0]['moves'] <= 0:
            return jsonify({'error': "Not enough moves to travel"}), 400

        # Select only stealable artifacts
        stealable_artifacts_list = [artifact for artifact in fetch_artifacts(item_id, game_id) if artifact["stealable"] == 1]
        # Check if a stealable artifact exists
        if len(stealable_artifacts_list) == 0:
            return jsonify({'error': 'Artifact not found'}), 404

        steal_artifact(item_id, game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({"message": "success"}), 200

@app.route('/games/<int:game_id>/artifacts', methods=['GET'])
def get_artifacts(game_id):
    try:
        result = fetch_artifacts(None, game_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(result), 200

# Endpoint to get airports, optionally within certain range
@app.route('/games/<int:game_id>/airports', methods=['GET'])
def player_find_airports(game_id):
    try:
        # Get & validate max distance
        max_distance_km = request.args.get('max_distance_km') # max_distance_km parameter is optional
        # Check is max_distance_km decimal, but only when max distance is defined
        if max_distance_km and not max_distance_km.isdecimal():
            return jsonify({'error': "max_distance_km must be a number"}), 400
        # If max_distance_km is defined, convert to the correct format
        if max_distance_km:
            max_distance_km = round(float(max_distance_km), 2)

        result = list_airports(game_id, max_distance_km)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

@app.route('/games/<int:game_id>/travel', methods=['GET', 'POST'])
def player_travel(game_id):
    try:
        # Get & validate ident
        arr_ident = request.args.get('arr_ident')
        if not is_ident(arr_ident):
            return jsonify({'error': "arr_ident must be a valid ident"}), 400

        # Fetch player by the given id
        player: list[dict[Any, Any]] = get_current_player(game_id)
        # Check if user exists
        if len(player) == 0:
            return jsonify({'error': "No player with given id found"}), 404

        # Check if player is at the requested airport already
        if player[0]['location'] == arr_ident:
            return jsonify({'error': "Given arr_ident must not be the same as player's location"}), 400

        # Fetch travel details
        travel_info: list[dict[Any, Any]] = fetch_travel_details(game_id, arr_ident)

        # Check if the airport of arrival was found
        if len(travel_info) == 0:
            return jsonify({'error': "No airport with given ident found"}), 404

        travel_price = travel_info[0]['travel_price']
        distance_km = travel_info[0]['distance_km']

        # Check if player has moves
        if player[0]['moves'] <= 0:
            return jsonify({'error': "Not enough moves to travel"}), 400

        # Compare player's balance and travel price
        if player[0]['balance'] < travel_price:
            return jsonify({'error': "Player does not have enough money to travel"}), 400

        if request.method == 'POST':
            # Travel to the airport
            travel(game_id, arr_ident, travel_price, distance_km)
            return jsonify({
                "message": "Player successfully travelled",
                "distance_km": distance_km,
                "travel_price": travel_price
            }), 200
        elif request.method == 'GET':
            return jsonify(travel_info[0]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid request method'}), 405

# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)