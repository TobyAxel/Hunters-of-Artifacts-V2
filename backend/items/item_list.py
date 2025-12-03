from backend.game_classes import *
from backend.items.item_functions import *
item_list = [
    Item('Hidden terminal pass',
       'Explore once without losing moves',
       False,
       0,
       'common',
       item_func),
    Item('Found terminal pass',
           'Do nothing loser',
           False,
           0,
           'common',
           item_func),

]