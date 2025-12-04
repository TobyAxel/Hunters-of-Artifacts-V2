from sql_connection import cursor
from events.events import *
import random

#---- HELPER FUNCTIONS ----#

def _rows_to_dicts(rows):
    cols = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in rows]

#---- GAME FUNCTIONS ----#

#---- GET ----#

def get_games(game_id = None):
    # Fetch games, optionally by id
    cursor.execute("SELECT * FROM game WHERE archived = false AND (%s is NULL OR id = %s)", (game_id, game_id))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    # convert datetime to iso format
    for res in results:
        res["created_at"] = res["created_at"].isoformat()
    return results

def get_players(game_id):
    cursor.execute("SELECT * FROM player WHERE game_id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)
    return results

def get_event(game_id):
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    results = _rows_to_dicts(rows)

    # Check if player is out of moves
    if results[0]['moves'] == 0 and results[0]['event_id'] is None:
        return "Not enough moves to explore more."

    # Check if there is an event already going on
    if results[0]['event_id'] is None:
        event_id = random.randint(0, len(event_list) - 1)
        cursor.execute("UPDATE game SET event_id = %s, event_state = 0, moves = moves - 1 WHERE id = %s", (event_id, game_id,))
        event = event_list[event_id]
        return event.states[0].text

    # Display existing event's state
    else:
        event = event_list[results[0]['event_id']]
        return event.states[results[0]['event_state']].text

 
  
#---- POST ----#

def create_new_game(data):
    # Get players and config
    [name, players, config] = [data.get('name'), data.get('players'), data.get('config')]

    # Create game
    cursor.execute(
        "INSERT INTO game (name, round, max_round, moves, modifier, archived) VALUES (%s, 1, %s, 2, %s, false)",
        (name, config['max_round'], config['modifier'])
    )
    new_game_id = cursor.lastrowid

    # Create players
    for player in players:
        cursor.execute("INSERT INTO player (game_id, distance_travelled, balance, location, screen_name) VALUES (%s, %s, %s, %s, %s)",
                       (new_game_id, config["starting_distance"], config["starting_balance"], config["starting_location"], player))

    # Set first player's turn
    cursor.execute('UPDATE game SET player_turn = (SELECT id FROM player WHERE game_id = %s LIMIT 1) WHERE id = %s', (new_game_id, new_game_id))

    # Return new game table state
    games = get_games()
    return games

def end_turn(game_id):
    # Get current player turn
    cursor.execute("SELECT player_turn FROM game WHERE id = %s", (game_id,))
    current_player_id = cursor.fetchone()[0]

    # Get all player ids in the game
    cursor.execute("SELECT id FROM player WHERE game_id = %s ORDER BY id", (game_id,))
    player_ids = [row[0] for row in cursor.fetchall()]

    # Determine next player's turn, we check index because player ids may not be sequential
    current_index = player_ids.index(current_player_id)
    next_index = (current_index + 1) % len(player_ids)
    next_player_id = player_ids[next_index]

    # Check if we completed a round
    round_passed = 1 if next_index == 0 else 0

    # Update game with next player's turn
    cursor.execute("UPDATE game SET player_turn = %s, round = round + %s, moves = 2 WHERE id = %s", (next_player_id, round_passed, game_id))

    # Return updated game state
    game = get_games(game_id)

    return game

def update_event(data, game_id):
    # Get option
    event_option = data.get('event_option') - 1

    # Get current event & state from db
    cursor.execute("SELECT event_id, event_state FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    event_in_db = _rows_to_dicts(rows)

    # Check if there is an active event
    if event_in_db[0]['event_id'] is None:
        return "No event is active."

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
