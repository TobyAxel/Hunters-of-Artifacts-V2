from sql_connection import cursor

## HELPER FUNCTIONS ##

def _rows_to_dicts(rows):
    cols = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in rows]

## GAME FUNCTIONS ##

def get_games():
    cursor.execute("SELECT * FROM game")
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

def get_game(game_id):
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

def create_new_game(data):
    [players, config] = [data.get('players'), data.get('config')]

    cursor.execute(
        "INSERT INTO game (round, max_round, moves, modifier, archived) VALUES (1, %s, 2, %s, false)",
        (config['max_round'], config['modifier'])
    )
    new_game_id = cursor.lastrowid

    for player in players:
        cursor.execute("INSERT INTO player (game_id, distance_travelled, balance, location, screen_name) VALUES (%s, %s, %s, %s, %s)",
                       (new_game_id, config["starting_distance"], config["starting_balance"], config["starting_location"], player))

    cursor.execute('UPDATE game SET player_turn = (SELECT id FROM player WHERE game_id = %s LIMIT 1) WHERE id = %s', (new_game_id, new_game_id))

    return new_game_id

def get_players(game_id):
    cursor.execute("SELECT * FROM player WHERE game_id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results