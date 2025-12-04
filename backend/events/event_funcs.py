from sql_connection import *

def add_money(amount, game_id):
    if amount < 0:
        got_lost = "lost"
    else:
        got_lost = "got"

    cursor.execute("UPDATE player set balance = balance + %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (amount,game_id,))

    return f"You {got_lost} {amount}€.\n"

def add_item(item, game_id):
    if item.rarity == 'artifact':
        cursor.execute("SELECT * FROM item WHERE rarity = 'artifact' WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_artifacts = cursor.fetchall()
        for artifact in owned_artifacts:
            if item.name == artifact[1]:
                return 'artifact is already owned!'
    cursor.execute("INSERT INTO item VALUES (DESCRIBE, %s, (SELECT player_turn FROM game WHERE id = %s), %s)", (item.name, game_id, item.rarity))
    return f"You gained a {item.name}"