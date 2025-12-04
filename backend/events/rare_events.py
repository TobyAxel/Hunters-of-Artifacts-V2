from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.item_list import *
import random

gambler_table_event = Event([
    State("You find a hidden gambling ring. A dealer invites you to wager 400€. Do you play?", [
        Choice("Yes", add_item_money, [gamblers_lucky_coin, 30, random.randint(-500, 500)], 2),
        Choice("No", None, None, 1),
    ]),
    State("You walk away from the shady table.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

lost_ticket_event = Event([
    State("You find a plane ticket lying on a bench. It’s valid for a short-distance flight. Take it?", [
        Choice("Yes", add_item_money, [extra_ticket, 85, 100], 2),
        Choice("No", None, None, 1),
    ]),
    State("You leave it. Maybe someone else will find it.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

strange_collector_event = Event([
    State("A Strange collector approaches you. He offers to buy one of your items at a 'good price'.", [
        Choice("Yes", sell_item, [600], 2),
        Choice("No", None, None, "final"),
    ]),
    State("You decline the collector's offer", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

abandoned_luggage_event = Event([
    State("You find some unclaimed luggage at a quiet station. take it?", [
        Choice("Yes", add_item_money, [energy_drink, 20, random.randint(0, 600)], 2),
        Choice("No", None, None, 1),
    ]),
    State("You decided to leave it be.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])