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
    [round, max_round, modifier] = [data.get('round'), data.get('max_round'), data.get('modifier')]

    cursor.execute(
        "INSERT INTO game (round, max_round, modifier) VALUES (%s, %s, %s)",
        (round, max_round, modifier)
    )
    new_game_id = cursor.lastrowid
    return new_game_id
