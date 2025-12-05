from backend.game_classes import *
from backend.events.event_funcs import *
from backend.items.item_list import *
import random

gambler_event = Event([
    State("You meet a gambler. Gamble?", [
        Choice("Yes",add_money, [random.randint(-1000, 1000)], 2),
        Choice("No", None, None, 1),
    ]),
    State("You choose not to partake in unauthorized gambling. Press enter to continue...", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue", None, None, "final"),
    ])
])

hidden_terminal_pass_event = Event([
    State("You spot a hidden terminal in the corner. Attempt to hack it?", [
        Choice("Yes", add_item, [hidden_terminal_pass], 2),
        Choice("No", None, None, 1)
    ]),
    State("You chose not to hack the terminal.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue", None, None, "final"),
    ])
])

cash_on_floor_event = Event([
    State("You find some cash on the floor. Do you want to pick it up?", [
        Choice("Yes", add_item_money, [discount_voucher, 50, 300], 2),
        Choice("No", None, None, 1),
    ]),
    State("You ignored the cash and walked away.", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue", None, None, "final"),
    ])
])

risky_stash_event = Event([
    State("A sealed package sits on a bench. Do you want to open it?", [
        Choice("Yes", add_item_money, [suspicious_package, 5, 400], 2),
        Choice("No", None, None, 1),
    ]),
    State("You leave the package untouched", [
        Choice("Continue", None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

energy_drink_event = Event([
    State("A vendor offers an energy drink for 400€. Do you want to buy it?", [
        Choice("Yes", buy_item, [energy_drink, 400], 2),
        Choice("No",None, None, 1),
    ]),
    State("You decline the offer.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

broken_atm_event = Event([
    State("You found a broken ATM. Do you want to try to break into it?", [
        Choice("Yes", add_money_chance, [500, 300, 70], 2),
        Choice("No", None, None, 1),
    ]),
    State("You decided not to break into the ATM.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

street_musician_event = Event([
    State("You see a street musician playing lively tunes. They're selling discount vouchers for 200€. Do you want to buy one?", [
        Choice("Yes", buy_item, [discount_voucher, 200], 2),
        Choice("No", None, None, 1),
    ]),
    State("The musician smiles and plays a song for you.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])

broken_vending_machine_event = Event([
    State("You see a broken wending machine. Check it out?", [
        Choice("Yes", add_item_money, [energy_drink, 25, 250], 2),
        Choice("No", None, None, 1),
    ]),
    State("You ignore the broken vending machine.", [
        Choice("Continue",None, None, "final"),
    ]),
    State("Press enter to continue...", [
        Choice("Continue",None, None, "final"),
    ])
])