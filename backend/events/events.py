from game_classes import *
from events.event_funcs import *
import random

gambler_event = Event([
    State("You meet a gambler. Gamble?", [
        Choice("Yes", add_money, [random.randint(-1000, 1000)], 2),
        Choice("No", None, None, 1),
    ]),
    State("You choose not to partake in unauthorized gambling.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue", None, None, "final"),
    ])
])

event_list = [
    gambler_event
]