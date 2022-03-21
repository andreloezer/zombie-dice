"""

    All the dice logic

"""


from random import choice
from config import DICE_TYPES
from strings import DiceStrings as Strings


# All Dice related logic
class Dice:
    def __init__(self, color):
        self.color = color
        self.side = None

    # Return all dice info
    def __repr__(self):
        value = self.side if self.side else Strings.unknown_side
        return Strings.repr(self.color, value)

    # Roll dice
    def roll_dice(self):
        # Randomly choose a side
        self.side = choice(DICE_TYPES[self.color])
