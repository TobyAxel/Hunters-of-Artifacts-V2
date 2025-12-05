from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.item_list import *
import random

auction_event = Event([
    State("You stumble upon an underground auction. A small crowd is bidding on unknown items. Do you want to bid 1000€?", [
        Choice("Yes", buy_item_chance, [magical_stopwatch, 1000, 50], 2),
        Choice("No", None, None, 1),
    ]),
    State("You leave before anyone notices you.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

terminal_of_faces_event = Event([
    State("You pass by an old terminal displaying flight data and traveller information. Investigate the terminal?", [
        Choice("Yes", add_item_money, [player_locator, 50, 5], 2),
        Choice("No", None, None, 1),
    ]),
    State("You decide to just walk away.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

forgotten_locker_event = Event([
    State("You come across a locked, dusty locker that seems like it hasn't been opened in years. Try to open it?", [
        Choice("Yes", add_item_money, [magical_stopwatch, 40, random.randint(800, 1200)], 2),
        Choice("No", None, None, 1),
    ]),
    State("You leave the locker alone.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

suspicious_individual_event = Event([
    State("As you walk past an alley, a shady individual calls out to you. Do you approach him?", [
        Choice("Yes", suspicious_individual_event_func, [finnicky_teleporter, 70, 80], 2),
        Choice("No", None, None, 1),
    ]),
    State("You ignore the man", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue ...", [
        Choice("Continue",None, None, "final"),
    ])
])