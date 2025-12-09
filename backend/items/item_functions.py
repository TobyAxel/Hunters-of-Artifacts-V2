from backend.sql_connection import *
import random

def item_func(game_id, name, duration, usable):
    return f'Used item {name}.'

def energy_drink_func(game_id, name, duration, usable):
    cursor.execute("UPDATE game SET moves = moves + 1 WHERE id = %s", (game_id,))
    return f'Used item {name}.'

def gambler_coin_func(game_id, name, duration, usable):
    roll = random.randint(1, 100)
    if roll <= 50:
        cursor.execute("SELECT id FROM active_effect WHERE player_id = (SELECT player_turn FROM game WHERE id = %s) AND effect_name = %s", (game_id, "Gambler's Lucky Coin Success"))
        effect = cursor.fetchall()
        if not effect:
            cursor.execute("INSERT INTO active_effect (effect_name, player_id, duration) VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)",("Gambler's Lucky Coin Success", game_id , 3))
            cursor.execute("UPDATE game SET moves = moves + 1 WHERE id = %s", (game_id,))
        else:
            cursor.execute("UPDATE active_effect SET duration = duration + 3 WHERE id = %s", (effect[0]))
    else:
        cursor.execute("SELECT id FROM active_effect WHERE player_id = (SELECT player_turn FROM game WHERE id = %s) AND effect_name = %s",(game_id, "Gambler's Lucky Coin Fail"))
        effect = cursor.fetchall()
        if not effect:
            cursor.execute("INSERT INTO active_effect (effect_name, player_id, duration) VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)",("Gambler's Lucky Coin Fail", game_id, 2))
            cursor.execute("UPDATE game SET moves = moves - 1 WHERE id = %s", (game_id,))
        else:
            cursor.execute("UPDATE active_effect SET duration = duration + 2 WHERE id = %s", (effect[0]))

    return f'Used item {name}.'

def magical_stopwatch_func(game_id, name, duration, usable):
    cursor.execute("SELECT id FROM active_effect WHERE player_id = (SELECT player_turn FROM game WHERE id = %s) AND effect_name = %s",(game_id, "Magical Stopwatch"))
    effect = cursor.fetchall()
    if not effect:
        cursor.execute("INSERT INTO active_effect (effect_name, player_id, duration) VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)",("Magical Stopwatch", game_id, 2))
        cursor.execute("UPDATE game SET moves = moves + 1 WHERE id = %s", (game_id,))
    else:
        cursor.execute("UPDATE active_effect SET duration = duration + 2 WHERE id = %s", (effect[0]))
    return f'Used item {name}.'