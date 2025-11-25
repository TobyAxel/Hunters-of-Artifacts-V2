from backend.sql_connection import *

def add_money(amount):
    if amount < 0:
        got_lost = "lost"
    else:
        got_lost = "got"

    cursor.execute("INSERT INTO player (balance) VALUES (%s)", (amount,))

    return f"You {got_lost} {amount}."