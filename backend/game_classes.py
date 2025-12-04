class Event:
    def __init__(self, states):
        self.states = states

class State:
    def __init__(self, text, choices):
        self.text = text
        self.choices = choices

class Choice:
    def __init__(self, function, arguments, next_state):
        self.function = function
        self.arguments = arguments or [] # Will break if no list at all given
        self.next_state = next_state

    def perform_func(self, game_id):
        return self.function(*self.arguments, game_id)

class Item:
    def __init__(self, name, description, usable, duration, rarity, func):
        self.name = name
        self.description = description
        self.usable = usable
        self.duration = duration
        self.rarity = rarity
        self.func = func

    def perform_func(self, game_id):
        return self.func(game_id, self.name, self.duration, self.usable)