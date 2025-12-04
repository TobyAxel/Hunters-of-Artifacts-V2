from game_classes import *
from items.item_functions import *

hidden_terminal_pass = Item(
      'Hidden Terminal Pass',
      'Explore once without losing moves.',
      False,
      0,
      'common',
      item_func,
)

energy_drink = Item(
      'Energy Drink',
      'Grants +1 move.',
      True,
      0,
      'common',
      item_func,
)

discount_voucher = Item(
      'Discount Voucher',
      'Flights for this turn are 20% cheaper. Multiple uses adds to duration.',
      True,
      1,
      'common',
      item_func,
)

extra_ticket = Item(
      'Extra Ticket',
      'Allows a flight under 1000km to be taken for free.',
      False,
      0,
      'rare',
      item_func,
)

gamblers_lucky_coin = Item(
      "Gambler's Lucky Coin",
      '50% chance to give +1 moves for 3 turns, 50% chance for -1 moves for 2 turns.\nMultiple uses adds to duration.',
      True,
      0,
      'rare',
      item_func,
)

player_locator = Item(
      'Player Locator',
      'Reveal the exact location of one person.',
      True,
      0,
      'epic',
      item_func,
)

magical_stopwatch = Item(
      'Magical Stopwatch',
      'Grants +1 move, and +1 move for next 2 turns. Multiple uses adds to duration.',
      True,
      2,
      'epic',
      item_func,
)

finnicky_teleporter = Item(
      'Finnicky Teleporter',
      '75% chance to teleport you to entered location, 25% chance to explode andskip your next turn.',
      True,
      0,
      'legendary',
      item_func,
)

suspicious_package = Item(
      'Suspicious Package',
      'While you feel an urge to hold onto it, you have no longer have a desire to open it. Usage unknown.',
      False,
      0,
      'legendary',
      item_func,
)

air_barons_ledger = Item(
      "The Air Baron's Ledger",
      'All flights you take cost 30% less. One of the legendary artifacts.',
      False,
      0,
      'artifact',
      item_func,
)

chrono_locket = Item(
      'Chrono Locket',
      'Grants +1 move every turn. One of the legendary artifacts.',
      False,
      0,
      'artifact',
      item_func,
)

vault_of_infinite_wealth = Item(
      'Vault of Infinite Wealth',
      'Grants +750€ every turn. One of the legendary artifacts.',
      False,
      0,
      'artifact',
      item_func,
)

prism_of_possibilities = Item(
      'Prism of Possibilities',
      'Grants +3 to luck modifier. One of the legendary artifacts.',
      False,
      0,
      'artifact',
      item_func,
)

item_list = [
      hidden_terminal_pass,
      discount_voucher,
      energy_drink,
      extra_ticket,
      gamblers_lucky_coin,
      player_locator,
      magical_stopwatch,
      finnicky_teleporter,
      suspicious_package,
      air_barons_ledger,
      chrono_locket,
      vault_of_infinite_wealth,
      prism_of_possibilities,
]