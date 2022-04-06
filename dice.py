"""Dice class.
"""


from random import choice
from typing import Union

from config import DICES
from strings import DiceStrings as Strings


class Dice:
    """Class to represent the dice.
    """

    def __init__(self, color: str) -> None:
        """Init dice instance. The dice start having no chosen side.

        :param color: Color of the dice representing its difficult.
        """
        self.color = color
        self.side: Union[str, None] = None

    def __repr__(self) -> str:
        """Return a string representing the dice in the game with its color and side.

        :return: String representing the dice.
        """
        return Strings.repr(self.color, self.side)

    def roll_dice(self) -> None:
        """Roll dice.
        Choose a side for the dice randomly.
        """
        self.side = choice(DICES[self.color].sides)

    def reset_side(self) -> None:
        """Reset dice side to None, it can be re-rolled.
        """
        self.side = None
