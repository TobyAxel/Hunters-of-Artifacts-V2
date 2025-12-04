from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.items import *
import random

auction_event = Event([
    State("You stumble upon an underground auction. A small crowd is bidding on unknown items. Do you want to bid 1000€?\n1. Yes\n2. No", [
        Choice(buy_item_chance, [magical_stopwatch, 1000, 50], 2),
        Choice(None, None, 1),
    ]),
    State("You leave before anyone notices you.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice(None, None, "final"),
    ])
])

terminal_of_faces_event = Event([
    State("You pass by an old terminal displaying flight data and traveller information. Investigate the terminal?\n1. Yes\n2. No", [
        Choice(add_item_money, [player_locator, 50, 5], 2),
        Choice(None, None, 1),
    ]),
    State("You decide to just walk away.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice(None, None, "final"),
    ])
])

forgotten_locker_event = Event([
    State("You come across a locked, dusty locker that seems like it hasn't been opened in years. Try to open it?\n1. Yes\n2. No", [
        Choice(add_item_money, [magical_stopwatch, 40, random.randint(800, 1200)], 2),
        Choice(None, None, 1),
    ]),
    State("You leave the locker alone", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice(None, None, "final"),
    ])
])

suspicious_individual_event = Event([
    State("As you walk past an alley, a shady individual calls out to you. Do you approach him?\n1. Yes\n2. No", [
        Choice(suspicious_individual_event_func, [finnicky_teleporter, 70, 80], 2),
        Choice(None, None, 1),
    ]),
    State("You ignore the man", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice(None, None, "final"),
    ])
])