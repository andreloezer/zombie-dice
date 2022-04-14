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
        self.__name = self.__ask_name()
        self.__score = 0

    def __str__(self) -> str:
        """Return a string representing the player with its name and score.

        :return: String representing the player.
        """
        return Strings.display_player(self.__name, self.__score)

    def get_name(self) -> str:
        """Returns player name.

        :return: String of the player name.
        """
        return self.__name

    def get_score(self) -> int:
        """Returns player score.

        :return: Player score.
        """
        return self.__score

    def add_to_score(self, score) -> None:
        """Add to player score.

        :param score: Turn score to add to the player total score.
        """
        self.__score += score

    @staticmethod
    def __ask_name() -> str:
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
