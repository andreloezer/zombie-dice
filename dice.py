"""

    All the dice logic

"""


from random import choice
from config import DICES
from strings import DiceStrings as Strings


# All Dice related logic
class Dice:
    def __init__(self, color):
        self.color = color
        self.side = None

    # Return all dice info
    def __repr__(self):
        return Strings.repr(self.color, self.side)

    # Roll dice
    def roll_dice(self):
        # Randomly choose a side
        self.side = choice(DICES[self.color].sides)
