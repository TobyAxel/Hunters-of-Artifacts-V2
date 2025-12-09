from backend.helper_functions import rows_to_dicts
from events.events import *
from events.event_funcs import *
from items.item_list import *
import random

#---- GAME FUNCTIONS ----#

#---- GET ----#

def get_games(game_id = None):
    # Fetch games, optionally by id
    cursor.execute("SELECT * FROM game WHERE archived = false AND (%s is NULL OR id = %s)", (game_id, game_id))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)
    # convert datetime to iso format
    for res in results:
        res["created_at"] = res["created_at"].isoformat()
    return results

def get_players(game_id):
    cursor.execute("SELECT * FROM player WHERE game_id = %s", (game_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)
    return results

def get_player(player_id):
    cursor.execute("SELECT * FROM player WHERE id = %s", (player_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)
    return results

def get_current_player(game_id):
    cursor.execute("SELECT * FROM player INNER JOIN game ON game.player_turn = player.id WHERE game.id = %s", (game_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)
    return results

def get_event(game_id):
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)

    # Check if there is no active event
    if results[0]['event_id'] is None:
        return "No active event."

    # Display existing event's state
    event = event_list[results[0]['event_id']]
    choices = {}

    for choice in event.states[results[0]['event_state']].choices:
        choices[len(choices) + 1] = choice.text

    return {"text": event.states[results[0]['event_state']].text, "choices": choices}

def get_items(player_id):
    cursor.execute("SELECT * FROM item WHERE player_id = %s", [player_id,])
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)

    for result in results:
        for item in item_list:
            if item.name == result['name']:
                result['description'] = item.description
                break

    return results

def get_active_effects(player_id):
    cursor.execute("SELECT * FROM active_effect WHERE player_id = %s", [player_id,])
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)

    return results

def get_game_artifacts(game_id):
    cursor.execute("SELECT player.screen_name, item.name FROM item INNER JOIN player WHERE player.id = item.player_id AND item.rarity = 'artifact' AND player.game_id = %s", (game_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)

    players = {}
    for result in results:
        if result['screen_name'] not in players:
            players[result['screen_name']] = []
        players[result['screen_name']].append(result['name'])

    return players

def get_shop_items(game):
    # Check what state shop is in
    (max_round, current_round) = (game['max_round'], game['round'])
    if current_round / max_round <= 0.25:
        include = ['common']
    elif current_round / max_round <= 0.5:
        include = ['common', 'rare']
    elif current_round / max_round <= 0.75:
        include = ['common', 'rare', 'epic']
    else:
        include = ['common', 'rare', 'epic', 'legendary']

    # Set item prices
    item_prices = {
        'common': 600,
        'rare': 1200,
        'epic': 1800,
        'legendary': 2400
    }

    # Create items into list
    items = []
    i = 0
    for item in item_list:
        if item.rarity != 'artifact' and item.rarity in include:
            items.append({'id': i, 'name': item.name, 'description': item.description, 'price': item_prices[item.rarity], 'rarity': item.rarity})
            i += 1

    return items

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

    lower_effects(current_player_id)

    # Get all player ids in the game
    cursor.execute("SELECT id FROM player WHERE game_id = %s ORDER BY id", (game_id,))
    player_ids = [row[0] for row in cursor.fetchall()]

    # Determine next player's turn, we check index because player ids may not be sequential
    current_index = player_ids.index(current_player_id)
    next_index = (current_index + 1) % len(player_ids)
    next_player_id = player_ids[next_index]

    # Check if we completed a round
    round_passed = 1 if next_index == 0 else 0

    #Check if player has gambler's lucky coin
    moves = 2
    cursor.execute("SELECT effect_name FROM active_effect WHERE player_id = %s", (next_player_id,))
    active_effects = rows_to_dicts(cursor.fetchall())
    for effect in active_effects:
        if effect["effect_name"] == "Gambler's Lucky Coin Success":
            moves += 1
            break
        elif effect["effect_name"] == "Gambler's Lucky Coin Fail":
            moves -= 1
            break

    #Check if player has magical stopwatch
    cursor.execute("SELECT effect_name FROM active_effect WHERE player_id = %s", (next_player_id,))
    active_effects = rows_to_dicts(cursor.fetchall())
    for effect in active_effects:
        if effect["effect_name"] == "Magical Stopwatch":
            moves += 1
            break

    #Check if player has artifacts
    cursor.execute("SELECT name FROM item WHERE player_id = %s", (next_player_id,))
    items = rows_to_dicts(cursor.fetchall())
    for item in items:
        if item["name"] == "Chrono Locket":
            moves += 1
        elif item["name"] == "Vault of Infinite Wealth":
            cursor.execute("UPDATE player SET balance = balance + 750 WHERE id = %s", (next_player_id,))

    # Update game with next player's turn
    cursor.execute("UPDATE game SET player_turn = %s, round = round + %s, moves = %s, event_id = NULL, event_state = NULL WHERE id = %s", (next_player_id, round_passed, moves, game_id))

    # Return updated game state
    game = get_games(game_id)

    return game

def lower_effects(player_id):
    cursor.execute("SELECT * FROM active_effect WHERE player_id = %s", (player_id,))
    effects = cursor.fetchall()

    for effect in effects:
        # Lower duration
        new_duration = effect[3] - 1

        if new_duration <= 0:
            cursor.execute("DELETE FROM active_effect WHERE id = %s", (effect[0],))
        else:
            cursor.execute("UPDATE active_effect SET duration = %s WHERE id = %s", (new_duration, effect[0],))

def use_player_item(item_name, game_id):
    # Get current player's turn
    cursor.execute("SELECT player_turn FROM game WHERE id = %s", (game_id,))
    current_player = cursor.fetchone()[0]

    # Check if player has item
    cursor.execute("SELECT * FROM item WHERE player_id = %s AND name = %s LIMIT 1", (current_player, item_name))
    item_id = cursor.fetchone()
    
    if item_id is None:
        return 'Player does not have item.'

    # Use item
    result = ""
    for item in item_list:
        if item.name == item_name:
            # Check if item is usable
            if item.usable is False:
                return 'Item is not usable.'
            
            # Remove item
            cursor.execute("DELETE FROM item WHERE id = %s", (item_id[0],))

            # Add item to active effects
            if item.name != "Gambler's Lucky Coin" and item.name != "Magical Stopwatch":
                cursor.execute("INSERT INTO active_effect (effect_name, player_id, duration) VALUES (%s, %s, %s)", (item.name, current_player, item.duration))

            result = item.perform_func(game_id)
            break
    
    return result

def update_event(data, game_id):
    # Get option
    event_option = data.get('event_option') - 1

    # Get current event & state from db
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    rows = cursor.fetchall()
    results = rows_to_dicts(rows)

    # Check if there is an active event
    if results[0]['event_id'] is None:

        #Check if player has hidden terminal pass
        move_cost = 1
        cursor.execute("SELECT effect_name FROM active_effect WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)",(game_id,))
        rows = cursor.fetchall()
        active_effects = rows_to_dicts(rows)
        for effect in active_effects:
            if effect["effect_name"] == "Hidden Terminal Pass":
                move_cost = 0
                cursor.execute("DELETE FROM active_effect WHERE effect_name = %s", (effect["effect_name"],))
                break

        # Check if player is out of moves
        if results[0]['moves'] == 0 and move_cost == 1:
            return "Not enough moves to explore more."

        # Start new event
        event_id = event_handler(game_id)
        cursor.execute("UPDATE game SET event_id = %s, event_state = 0, moves = moves - %s WHERE id = %s", (event_id, move_cost, game_id,))
        
        # Get event and choices
        event = event_list[event_id]
        choices = {}
        for choice in event.states[0].choices:
            choices[len(choices) + 1] = choice.text

        # Return first event state text and choices
        return {"text": event.states[0].text, "choices": choices}

    # Get current event, current event state, event choice
    current_event = event_list[results[0]['event_id']]
    event_state = current_event.states[results[0]['event_state']]
    event_choice = event_state.choices[event_option]

    # Perform choice function if function is given and update new state to db
    flavor = ""
    if event_choice.function is not None:
        flavor = event_choice.perform_func(game_id)
    if event_choice.next_state == "final":
        cursor.execute("UPDATE game SET event_id = NULL, event_state = NULL WHERE id = %s", (game_id,))
        return "final"
    else:
        cursor.execute("UPDATE game SET event_state = %s WHERE id = %s", (event_choice.next_state, game_id))
        # Get new event choices
        choices = {}
        for choice in current_event.states[event_choice.next_state].choices:
            choices[len(choices) + 1] = choice.text
        # Flavor text from whatever event did and new event state
        final_string = f"{flavor}{current_event.states[event_choice.next_state].text}"
        return {"text": final_string, "choices": choices}

def buy_item(item_id, shop_items, game):
    # alert if item out of bounds
    if item_id >= len(shop_items):
        return 'item id outside of bounds'

    # Get what item player wants to buy
    item_to_buy = shop_items[item_id]

    # Get player balance
    cursor.execute("SELECT balance FROM player WHERE id = %s", (game['player_turn'],))
    balance = cursor.fetchone()[0]

    if balance < item_to_buy['price']:
        return 'You do not have enough money to buy this item'

    # Remove the money
    cursor.execute("UPDATE player SET balance = balance - %s WHERE id = %s", (item_to_buy['price'], game['player_turn']))

    # Add the item
    cursor.execute("INSERT INTO item VALUES (DEFAULT, %s, %s, %s)", (item_to_buy['name'], game['player_turn'], item_to_buy['rarity']))
    print('bought item')
    return 'successfully bought item'