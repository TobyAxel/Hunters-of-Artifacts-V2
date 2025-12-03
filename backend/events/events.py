from backend.game_classes import *
from backend.events.event_funcs import *
import random

gambler_event = Event([
    State("You meet a gambler. Gamble?\n1. Yes\n2. No", [
        Choice(add_money, [random.randint(-1000, 1000)], 2),
        Choice(None, None, 1),
    ]),
    State("You choose not to partake in unauthorized gambling.\nPress enter to continue...", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

event_list = [
    gambler_event
]