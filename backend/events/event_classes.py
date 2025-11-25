class Event:
    def __init__(self, states):
        self.states = states

class State:
    def __init__(self, text, choices):
        self.text = text
        self.choices = choices

    def __str__(self):
        return self.text

    def perform_choice(self, choice):
        return self.choices[choice]

class Choice:
    def __init__(self, function, arguments, next_state):
        self.function = function
        self.arguments = arguments
        self.next_state = next_state

    def perform_func(self):
        return self.function(*self.arguments)