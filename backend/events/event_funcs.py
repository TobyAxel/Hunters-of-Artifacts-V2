from backend.sql_connection import *

def add_money(amount, game_id):
    if amount < 0:
        got_lost = "lost"
    else:
        got_lost = "got"

    cursor.execute("UPDATE player set balance = balance + %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (amount,game_id,))

    return f"You {got_lost} {amount}€."