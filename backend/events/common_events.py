from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.items import *
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

hidden_terminal_pass_event = Event([
    State("You spot a hidden terminal in the corner. Attempt to hack it?\n1. Yes\n2. No", [
        Choice(add_item, [hidden_terminal_pass], 2),
        Choice(None, None, 1)
    ]),
    State("You chose not to hack the terminal.\nPress enter to continue...", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

cash_on_floor_event = Event([
    State("You find some cash on the floor. Do you want to pick it up?\n1. Yes\n2. No", [
        Choice(add_item_money, [discount_voucher, 50, 300], 2),
        Choice(None, None, 1),
    ]),
    State("You ignored the cash and walked away.\nPress enter to continue...", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

risky_stash_event = Event([
    State("A sealed package sits on a bench. Do you want to open it?\n1. Yes\n2. No", [
        Choice(add_item_money, [suspicious_package, 5, 400], 2),
        Choice(None, None, 1),
    ]),
    State("You leave the package untouched", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

energy_drink_event = Event([
    State("A vendor offers an energy drink for 400€. Do you want to buy it?\n1. Yes\n2. No", [
        Choice(buy_item, [energy_drink, 400], 2),
        Choice(None, None, 1),
    ]),
    State("You decline the offer.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

broken_atm_event = Event([
    State("You found a broken ATM. Do you want to try to break into it?\n1. Yes\n2. No", [
        Choice(add_money_chance, [500, 300, 70], 2),
        Choice(None, None, 1),
    ]),
    State("You decided not to break into the ATM.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

Street_musician_event = Event([
    State("You see a street musician playing lively tunes. Tip them 200€?\n1. Yes\n2. No", [
        Choice(buy_item, [discount_voucher, 200], 2),
        Choice(None, None, 1),
    ]),
    State("The musician smiles and plays a song for you.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])

broken_vending_machine_event = Event([
    State("You see a broken wending machine. Check it out?\n1. Yes\n2. No", [
        Choice(add_item_money, [Energy_drink, 25, 250], 2),
        Choice(None, None, 1),
    ]),
    State("You ignore the broken vending machine.", [
        Choice(None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice(None, None, "final"),
    ])
])