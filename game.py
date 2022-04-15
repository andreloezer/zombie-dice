"""Game class and related logic.
"""


from random import randrange, shuffle

from player import Player
from dice import Dice
from turn import Turn
from strings import GameStrings as Strings
from config import DICES, SCORE_LIMIT, MIN_PLAYERS, MAX_PLAYERS
from utils import int_input, bool_input, clear_console, stringify


# Store game states
class GameStates:
    """Class to store game states.
    """
    SETUP = "setup"
    GAME = "game"
    DRAW = "draw"
    END = "end"


class Game:
    """Class representing the game.
    """

    def __init__(self) -> None:
        """Init game class."""
        self.__players: list[Player] = []
        self.__dice_pool: list[Dice] = []
        self.__winners: list[Player] = []
        self.__round_count = 0
        self.__highest_score = 0
        self.__state = GameStates.SETUP
        self.__game_loop()

    def take_dice(self) -> Dice:
        """Pop 1 dice from the dice pool and return it.

        :return: Single dice.
        """
        return self.__dice_pool.pop(randrange(0, len(self.__dice_pool)))

    def return_dice(self, dice: Dice) -> None:
        """Return dice to the dice pool.

        :param dice: Dice to return to the dice pool.
        """
        self.__dice_pool.append(dice)

    def get_round_count(self) -> int:
        """Returns current round count.

        :return: Number of the current round count.
        """
        return self.__round_count

    def get_dice_pool_len(self) -> int:
        """Returns current length of the dice pool.

        :return: Length of the dice pool.
        """
        return len(self.__dice_pool)

    def shuffle_dice_pool(self) -> None:
        """Shuffle dices in the dice pool.
        """
        shuffle(self.__dice_pool)

    def __create_dices(self) -> None:
        """Create dices and fill the dice pool.
        """
        self.__dice_pool.clear()
        for dice_type in DICES:
            # Create dices of each color
            for i in range(DICES[dice_type].amount):
                dice = Dice(dice_type)
                self.__dice_pool.append(dice)

        self.shuffle_dice_pool()  # Shuffle dices in dice pool

    def display_dices(self) -> None:
        """Show dices in the dice pool.
        """
        print(Strings.display_dices(self.__dice_pool))

    def __setup_game(self) -> None:
        """Setup game, players and dices.
        """
        clear_console()
        print(Strings.greet_user())  # Greet user
        self.__create_dices()  # Create dices
        self.__create_players()   # Create players
        self.__state = GameStates.GAME  # Change state to GAME

    def __create_players(self) -> None:
        """Ask players names, create and store them.
        """
        number_of_players = int_input(Strings.ask_num_players, MIN_PLAYERS, MAX_PLAYERS)  # Ask number of players
        for player in range(number_of_players):
            self.__players.append(Player())

    def __end_game(self) -> None:
        """End game. Show players score and congrats winner.
        """
        print(Strings.end_game_players(stringify(self.__players), self.__winners[0].get_name()))
        input(Strings.end_game)
        clear_console()
        answer = bool_input(Strings.ask_continue)  # Ask if user wants to play again
        if answer:
            self.__reset_game()  # Set game for next play
        else:
            quit()  # Exit game

    def __reset_game(self) -> None:
        """Reset game memory back to initialization.
        """
        self.__players.clear()
        self.__dice_pool.clear()
        self.__winners.clear()
        self.__highest_score = 0
        self.__round_count = 0
        self.__state = GameStates.SETUP

    def __game_round(self, players: list[Player]) -> None:
        """Run a game turn, looping through all players.
        """
        self.__round_count += 1
        for player in players:
            Turn(self, player)
            self.__create_dices()
            if player.get_score() > self.__highest_score:
                self.__highest_score = player.get_score()  # Update the highest score in the game

        # Check if someone wins or if it's a draw
        self.__winners.clear()
        if self.__highest_score >= SCORE_LIMIT:
            for player in players:
                if player.get_score() == self.__highest_score:
                    self.__winners.append(player)  # Save each player that reached the highest score
                    self.__state = GameStates.DRAW
        if self.__winners and len(self.__winners) < 2:
            # There is only one player with the highest score
            self.__state = GameStates.END
        else:
            print(Strings.draw(stringify(self.__winners)))  # Inform the user there is a draw

    def __game_loop(self) -> None:
        """All the game happens inside this loop.
        It controls the flow of the game.
        """
        while True:
            match self.__state:
                case GameStates.SETUP:
                    self.__setup_game()  # Set the game up
                case GameStates.GAME:
                    self.__game_round(self.__players)  # Game turn with all players
                case GameStates.DRAW:
                    self.__game_round(self.__winners)  # Game turn with draw players
                case GameStates.END:
                    self.__end_game()  # End the game
