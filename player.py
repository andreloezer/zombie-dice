"""Player class and related logic.
"""


from strings import PlayerStrings as Strings
from utils import bool_input, text_input


class Player:
    """Class representing the player.
    """

    def __init__(self) -> None:
        """Init player.
        """
        self.name = self.ask_name()
        self.score = 0

    def __repr__(self) -> str:
        """Return a string representing the player with its name and score.

        :return: String representing the player.
        """
        return Strings.repr_player(self.name, self.score)

    @staticmethod
    def ask_name() -> str:
        """Ask the name of the player.

        :return: String of the player name.
        """
        return text_input(Strings.ask_name)

    @staticmethod
    def ask_continue(get_dices_amount: int) -> bool:
        """Ask if player wants to continue playing more hands in the current turn.

        :param get_dices_amount: Amount of dices to get from the dice pool.
        :return: Boolean if player wants or not to continue playing the turn.
        """
        return bool_input(Strings.ask_continue(get_dices_amount))
