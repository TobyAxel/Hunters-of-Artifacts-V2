from sql_connection import cursor

def get_games():
    cursor.execute("SELECT * FROM game")
    results = cursor.fetchall()
    print(f"Query executed. Row count: {cursor.rowcount}")
    print(f"Results: {results}")
    print(f"Cursor description: {cursor.description}")
    return results

def get_game(game_id):
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    results = cursor.fetchall()
    print(f"Query executed. Row count: {cursor.rowcount}")
    print(f"Results: {results}")
    print(f"Cursor description: {cursor.description}")
    return results