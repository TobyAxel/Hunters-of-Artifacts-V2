from placeholder_data import games

def get_games():
    return games

def get_game(game_id):
    for game in games:
        if game['id'] == game_id:
            return game
    return None