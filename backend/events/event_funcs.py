from backend.sql_connection import *
from backend.items.item_list import *
import random

#Function adds or deducts money
def add_money(amount, game_id):
    if amount < 0:
        got_lost = "lost"
    else:
        got_lost = "got"

    cursor.execute("UPDATE player set balance = balance + %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (amount,game_id,))

    return f"You {got_lost} {amount}€.\n"

#Function adds or deducts money based on chance
def add_money_chance(amount_won, amount_lost, chance, game_id):
    roll = random.randint(1, 100)
    if roll < chance:
        cursor.execute("UPDATE player set balance = balance + %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount_won,game_id))
        return f"You got {amount_won}€.\n"
    else:
        cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount_lost, game_id,))
        return f"You lost {amount_lost}€.\n"

#Function adds an item
def add_item(item, game_id):
    if item.rarity == 'artifact':
        cursor.execute("SELECT * FROM item WHERE rarity = 'artifact' WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_artifacts = cursor.fetchall()
        for artifact in owned_artifacts:
            if item.name == artifact[1]:
                return 'artifact is already owned!'
    cursor.execute("INSERT INTO item VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)", (item.name, game_id, item.rarity))
    return f"You gained a {item.name}\n"

#Function adds an item or money based on chance
def add_item_money(item, chance, amount, game_id):
    roll = random.randint(1, 100)
    if roll <= chance:
        add_item(item, game_id)
    else:
        add_money(amount, game_id)

#Function adds an item and deducts the money for it
def buy_item(item, amount, game_id):
    cursor.execute("SELECT balance FROM player WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (amount,game_id,))
    balance = cursor.fetchall()
    if balance >= amount:
        cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount, game_id,))
        cursor.execute("INSERT INTO item VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)",(item.name, game_id, item.rarity))
        return f"You bought {item.name} for {amount}€."
    else:
        return "You don't have enough money."

#Function adds an item and deducts the money for it based on chance
def buy_item_chance(item, amount, chance, game_id):
    cursor.execute("SELECT balance FROM player WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (amount,game_id,))
    balance = cursor.fetchall()
    if balance >= amount:
        roll = random.randint(1, 100)
        if roll <= chance:
            cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount, game_id,))
            cursor.execute("INSERT INTO item VALUES (%s, (SELECT player_turn FROM game WHERE id = %s), %s)",(item.name, game_id, item.rarity))
            return f"You bought {item.name} for {amount}€."
        else:
            return "You lose the bid, but dont lose money."
    else:
        return "You don't have enough money."

#Function deducts an item and adds the money for it
def sell_item(amount, game_id):
    cursor.execute("SELECT * FROM item WHERE rarity = 'common' AND player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    item = cursor.fetchone
    if item.len > 0:
        cursor.execute("DELETE FROM item WHERE player_id = (SELECT player_turn FROM game WHERE id = %s) AND name = &s LIMIT 1", (game_id, item))
        return add_money(amount, game_id)
    else:
        return "You have no items to sell."

#Function is only for suspicious_individual_event
def suspicious_individual_event_func(item, chance1, chance2, game_id):
    roll = random.randint(1, 100)
    if roll <= chance1:
        cursor.execute("SELECT * FROM item WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_items = cursor.fetchall()
        for items in owned_items:
            if items.name == "Suspicious Package":
                #Get all artifacts
                artifacts = []
                for Item.name, Item.rarity in item_list:
                    if Item.rarity == 'artifact':
                        artifacts.append(Item.name)
                #Remove owned artifacts from artifact pool
                cursor.execute("SELECT * FROM item WHERE rarity = 'artifact' WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)",(game_id,))
                owned_artifacts = cursor.fetchall()
                for artifact in artifacts[:]:
                    if artifact in owned_artifacts:
                        artifacts.remove(artifact)
                if len(artifacts) == 0:
                    return add_money(1750, game_id)
                else:
                    artifact = random.choice(artifacts)
                    return add_item(artifact, game_id)
            else:
                return add_money(1000, game_id)
    elif roll <= chance2:
        return add_money(-500, game_id)
    else:
        return add_item(item, game_id)

def add_artifact(chance, chance2, amount, amount2, game_id):
    roll = random.randint(1, 100)
    if roll <= chance:
        return add_money(amount, game_id)
    elif roll <= chance2:
        artifacts = []
        for Item.name, Item.rarity in item_list:
            if Item.rarity == 'artifact':
                artifacts.append(Item.name)
        # Remove owned artifacts from artifact pool
        cursor.execute(
            "SELECT * FROM item WHERE rarity = 'artifact' WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)",
            (game_id,))
        owned_artifacts = cursor.fetchall()
        for artifact in artifacts[:]:
            if artifact in owned_artifacts:
                artifacts.remove(artifact)
        if len(artifacts) == 0:
            return add_money(amount2, game_id)
        else:
            artifact = random.choice(artifacts)
            return add_item(artifact, game_id)
    else:
        return "You gain nothing"