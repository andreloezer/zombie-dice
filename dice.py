"""Dice class.
"""


from random import choice
from typing import Union

from config import DICES
import strings


class Dice:
    """Class to represent the dice.
    """

    def __init__(self, color: str) -> None:
        """Init dice instance. The dice start having no chosen side.

        :param color: Color of the dice representing its difficult.
        """
        self.__color = color
        self.__side: Union[str, None] = None

    def __str__(self) -> str:
        """Return a string representing the dice in the game with its color and side.

        :return: String representing the dice.
        """
        return strings.DiceStrings.display_dice(self.__color, self.__side)

    def roll_dice(self) -> None:
        """Roll dice.
        Choose a side for the dice randomly.
        """
        self.__side = choice(DICES[self.__color].sides)

    def reset_side(self) -> None:
        """Reset dice side to None, it can be re-rolled.
        """
        self.__side = None

    @property
    def color(self) -> str:
        """Return dice color.

        :return: String of the dice color.
        """
        return self.__color

    @property
    def value(self) -> str:
        """Return dice rolled value.

        :return: String of the dice rolled value.
        """
        return self.__side
