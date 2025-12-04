from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.item_list import *
import random

ancient_vault_event = Event([
    State("You discover an ancient vault deep underground. The vault door has a symbol of some of ancient device. Do you want to try to open to vault?", [
        Choice("Yes", add_item_money, [finnicky_teleporter, 50, random.randint(1500,2500)], 2),
        Choice("No", None, None, "1"),
    ]),
    State("You decide to leave the vault for someone else", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue", None, None, "final"),
    ])
])

locked_briefcase_event = Event([
    State("You come across a locked briefcase that looks valuable. Do you want to try to open it?", [
        Choice("Yes", add_money_chance, [random.randint(2554, 2985), -500, 70], 2),
        Choice("No", None, None, "1"),
    ]),
    State("You decide not to mess with the briefcase.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue", None, None, "final"),
    ])
])

data_vault_event = Event([
    State("You find a high-security server room still powered deep underground. Do you wabt to try  to hack the data vault?", [
        Choice("Yes", add_money_chance, [random.randint(1000, 3000), -500, 50], 2),
        Choice("No", None, None, "1"),
    ]),
    State("You walk away, leaving  the server untouched.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue", None, None, "final"),
    ])
])

abandoned_space_pod_event = Event([
    State("You find a half-buried escape pod in a scrapyard, it's lights still flickering faintly. Do you want to investigate the pod?", [
        Choice("Yes", add_artifact, [45, 80, 2000, 5000], 2),
        Choice("No", None, None, "1"),
    ]),
    State("You leave the pod alone.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue", None, None, "final"),
    ])
])

time_capsule_event = Event([
    State("You uncover a sealed time capsule marked 'open  in 2200. Do you want to open in now?", [
        Choice("Yes", add_artifact, [45, 80, 2500, 5000], 2),
        Choice("No", None, None, "1"),
    ]),
    State("You leave the time capsule undisturbed.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue", None, None, "final"),
    ])
])