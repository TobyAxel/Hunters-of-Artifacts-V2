from sql_connection import cursor
from decorator import append
import random


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


def get_event(game_id, event_list, event):
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    event_list = event_list[0]
    # Check if player is out of moves
    if results[0]['moves'] == 0 and results[0]['event_id'] is None:
        return "Not enough moves to explore more."

    # Check if there is an event already going on
    if results[0]['event_id'] is None:
        event_id = random.randint(0, len(event_list - 1))
        cursor.execute("UPDATE game SET event_id = %s, event_state = 0, moves = moves - 1 WHERE id = %s", (event_id, game_id),)
        event = event_list[event_id]
        return event.states[0].text

    # Display existing event's state
    else:
        event = event_list[results[0]['event_id']]
        return event.states[results[0]['event_state']].text

 
  
#---- POST ----#

def create_new_game(data):
    # Get players and config
    [players, config] = [data.get('players'), data.get('config')]

    # Create game
    cursor.execute("INSERT INTO game (round, max_round, moves, modifier, archived) VALUES (1, %s, 2, %s, false)",
    (config['max_round'], config['modifier']))
    new_game_id = cursor.lastrowid

    # Create players
    for player in players:
        cursor.execute("INSERT INTO player (game_id, distance_travelled, balance, location, screen_name) VALUES (%s, %s, %s, %s, %s)",
                       (new_game_id, config["starting_distance"], config["starting_balance"], config["starting_location"], player))

    # Set first player's turn
    cursor.execute('UPDATE game SET player_turn = (SELECT id FROM player WHERE game_id = %s LIMIT 1) WHERE id = %s', (new_game_id, new_game_id))
    return new_game_id

def get_players(game_id):
    cursor.execute("SELECT * FROM player WHERE game_id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

def get_player(player_id):
    cursor.execute("SELECT * FROM player WHERE id = %s", (player_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

def event(game_id, event_in_db, event_list, event_option):
    # Get current event, current event state, event choice
    current_event = event_list[event_in_db[0]['event_id']]
    event_state = current_event.states[event_in_db[0]['event_state']]
    event_choice = event_state.choices[event_option]

    # Perform choice function if function is given and update new state to db
    flavor = ""
    if event_choice.function is not None:
        flavor = event_choice.perform_func(game_id)
    if event_choice.next_state == "final":
        cursor.execute("UPDATE game SET event_id = NULL, event_state = NULL WHERE id = %s", (game_id,))
        return ""
    else:
        cursor.execute("UPDATE game SET event_state = %s WHERE id = %s", (event_choice.next_state, game_id))
        # Flavor text from whatever event did and new event state
        final_string = f"{flavor}{current_event.states[event_choice.next_state].text}"
        return final_string

def get_items(player_id):
    cursor.execute(f"SELECT * FROM item WHERE player_id = {player_id}")
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

