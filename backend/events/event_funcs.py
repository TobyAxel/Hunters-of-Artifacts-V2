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

    return f"You {got_lost} {amount}€. "

#Function adds or deducts money based on chance
def add_money_chance(amount_won, amount_lost, chance, game_id):
    roll = random.randint(1, 100)
    if roll < chance:
        cursor.execute("UPDATE player set balance = balance + %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount_won,game_id))
        return f"You got {amount_won}€. "
    else:
        cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount_lost, game_id,))
        return f"You lost {amount_lost}€. "

#Function adds an item
def add_item(item, game_id):
    if item.rarity == 'artifact':
        cursor.execute("SELECT * FROM item WHERE rarity = 'artifact' AND player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_artifacts = cursor.fetchall()
        for artifact in owned_artifacts:
            if item.name == artifact[1]:
                return 'artifact is already owned!'
    cursor.execute("INSERT INTO item VALUES (DEFAULT, %s, (SELECT player_turn FROM game WHERE id = %s), %s)", (item.name, game_id, item.rarity))
    return f"You gained {item.name}. "

#Function adds an item or money based on chance
def add_item_money(item, chance, amount, game_id):
    roll = random.randint(1, 100)
    if roll <= chance:
        return add_item(item, game_id)
    else:
        return add_money(amount, game_id)

#Function adds an item and deducts the money for it
def buy_item(item, amount, game_id):
    cursor.execute("SELECT balance FROM player WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount, game_id,))
        cursor.execute("INSERT INTO item VALUES (DEFAULT, %s, (SELECT player_turn FROM game WHERE id = %s), %s)",(item.name, game_id, item.rarity))
        return f"You bought {item.name} for {amount}€. "
    else:
        return "You don't have enough money. "

#Function adds an item and deducts the money for it based on chance
def buy_item_chance(item, amount, chance, game_id):
    cursor.execute("SELECT balance FROM player WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        roll = random.randint(1, 100)
        if roll <= chance:
            cursor.execute("UPDATE player set balance = balance - %s WHERE id = (SELECT player_turn FROM game WHERE id = %s)",(amount, game_id,))
            cursor.execute("INSERT INTO item VALUES (DEFAULT, %s, (SELECT player_turn FROM game WHERE id = %s), %s)",(item.name, game_id, item.rarity))
            return f"You bought {item.name} for {amount}€. "
        else:
            return "You lose the bid, but dont lose money. "
    else:
        return "You don't have enough money. "

#Function deducts an item and adds the money for it
def sell_item(amount, game_id):
    cursor.execute("SELECT * FROM item WHERE rarity = 'common' AND player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    items = cursor.fetchall()

    if not items:
        return "You have no items to sell. "

    item = items[0]

    if item[3] is not None:
        cursor.execute("DELETE FROM item WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)AND rarity = %s LIMIT 1", (game_id, item[3]))
        return add_money(amount, game_id)

    return "You have no items to sell. "

#Function is only for suspicious_individual_event
def suspicious_individual_event_func(item, chance1, chance2, game_id):
    roll = random.randint(1, 100)
    if roll <= chance1:
        cursor.execute("SELECT * FROM item WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_items = cursor.fetchall()
        for items in owned_items:
            if items[1] == "Suspicious Package": # SQL returns tuple, not dict
                #Get all artifacts
                artifacts = []
                for item2 in item_list:
                    if item2.rarity == 'artifact':
                        artifacts.append(item2)

                #Remove owned artifacts from artifact pool
                cursor.execute("SELECT name FROM item WHERE rarity = 'artifact' AND player_id = (SELECT player_turn FROM game WHERE id = %s)",(game_id,))
                owned_artifacts_raw = cursor.fetchall()

                # Turn the query into usable list
                owned_artifacts = []
                for owned_artifact in owned_artifacts_raw:
                    owned_artifacts.append(owned_artifact[0])

                # Put unowned artifacts in their own list, as removing from a list we are iterating over
                # Breaks stuff
                unowned_artifacts = []
                for artifact in artifacts:
                    if artifact.name not in owned_artifacts:
                        unowned_artifacts.append(artifact)

                if len(unowned_artifacts) == 0:
                    return add_money(1750, game_id)
                else:
                    artifact = random.choice(unowned_artifacts)
                    return add_item(artifact, game_id)

        return add_money(1000, game_id) # Needs to be outside for loop, instantly gives this if first item not suspicious package
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
        for item2 in item_list:
            if item2.rarity == 'artifact':
                artifacts.append(item2)
        # Remove owned artifacts from artifact pool
        cursor.execute("SELECT name FROM item WHERE rarity = 'artifact' AND player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
        owned_artifacts_raw = cursor.fetchall()

        # Turn the query into usable list
        owned_artifacts = []
        for owned_artifact in owned_artifacts_raw:
            owned_artifacts.append(owned_artifact[0])

        # Put unowned artifacts in their own list, as removing from a list we are iterating over
        # Breaks stuff
        unowned_artifacts = []
        for artifact in artifacts:
            if artifact.name not in owned_artifacts:
                unowned_artifacts.append(artifact)

        if len(unowned_artifacts) == 0:
            return add_money(amount2, game_id)
        else:
            artifact = random.choice(unowned_artifacts)
            return add_item(artifact, game_id)
    else:
        return "You gain nothing. "