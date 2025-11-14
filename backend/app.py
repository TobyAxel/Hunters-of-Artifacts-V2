from flask import Flask, request
from placeholder_data import games
app = Flask(__name__)

@app.route('/games', methods=['GET'])
def fetch_games():
    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def fetch_game(game_id):
    game = games[game_id]
    return jsonify(game)

# Run backend
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)