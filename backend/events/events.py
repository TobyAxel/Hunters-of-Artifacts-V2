from backend.events.common_events import *
from backend.events.rare_events import *
from backend.events.epic_events import *
from backend.events.legendary_events import *
import random

def event_handler(game_id):
    #Default chances
    common = 55
    rare = 75
    epic = 90
    legendary = 100

    #Luck  multiplier based on distance travelled
    cursor.execute("SELECT distance_travelled FROM player WHERE id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    distance_raw = cursor.fetchone()
    distance = distance_raw[0]
    distance_multiplier = distance // 2000 + 1
    cursor.execute("SELECT modifier FROM game WHERE  id = %s", (game_id,))
    game_modifier_raw = cursor.fetchone()
    game_modifier = game_modifier_raw[0]
    modifier = game_modifier * distance_multiplier

    #Check if prism of possibilities is active
    cursor.execute("SELECT effect_name FROM active_effect WHERE player_id = (SELECT player_turn FROM game WHERE id = %s)", (game_id,))
    active_effects = cursor.fetchall()
    for effect in active_effects:
        if effect[0] == "prism_of_possibilities":
            modifier += 3

    #Roll cap based on distance travelled
    if distance < 1250 // modifier:
        max_roll = 60
    elif distance < 2500 // modifier:
        max_roll = 80
    elif distance < 4500 // modifier:
        max_roll = 91
    else:
        max_roll = 100

    #Roll for event rarity
    roll = 0
    for i in range(0, int(modifier)):
        reroll = random.randint(0, max_roll)
        if reroll > roll:
            roll = reroll

    #Gets event rarity based on roll
    if roll <= common:
        return  random.randint(0, len(common_event_list) -1)
    elif roll <= rare:
        return random.randint(0, len(rare_event_list) +7)
    elif roll <= epic:
        return random.randint(0, len(epic_event_list) +11)
    elif roll <= legendary:
        return random.randint(0, len(legendary_event_list) +15)


common_event_list = [
    gambler_event,
    hidden_terminal_pass_event,
    cash_on_floor_event,
    risky_stash_event,
    energy_drink_event,
    broken_atm_event,
    street_musician_event,
    broken_vending_machine_event,
]

rare_event_list = [
    gambler_table_event,
    lost_ticket_event,
    strange_collector_event,
    abandoned_luggage_event,
]

epic_event_list = [
    auction_event,
    terminal_of_faces_event,
    forgotten_locker_event,
    suspicious_individual_event,
]

legendary_event_list = [
    ancient_vault_event,
    locked_briefcase_event,
    data_vault_event,
    abandoned_space_pod_event,
    time_capsule_event
]

event_list = [
    gambler_event,
    hidden_terminal_pass_event,
    cash_on_floor_event,
    risky_stash_event,
    energy_drink_event,
    broken_atm_event,
    street_musician_event,
    broken_vending_machine_event,
    gambler_table_event,
    lost_ticket_event,
    strange_collector_event,
    abandoned_luggage_event,
    auction_event,
    terminal_of_faces_event,
    forgotten_locker_event,
    suspicious_individual_event,
    ancient_vault_event,
    locked_briefcase_event,
    data_vault_event,
    abandoned_space_pod_event,
    time_capsule_event
    ]