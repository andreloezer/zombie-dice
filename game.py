"""Game class and related logic.
"""


from random import randint, shuffle


from dice import Dice
from player import Player
from strings import GameStrings as Strings
from config import DICES, SCORE_LIMIT, MIN_PLAYERS, MAX_PLAYERS
from utils import int_input, text_input, bool_input, clear_console


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
        self.players: list[Player] = []
        self.dice_pool: list[Dice] = []
        self.winners: list[Player] = []
        self.highest_score = 0
        self.state = GameStates.SETUP
        self.game_loop()

    def take_dice(self) -> Dice:
        """Pop 1 dice from the dice pool and return it.

        :return: Single dice.
        """
        return self.dice_pool.pop(randint(0, (len(self.dice_pool) - 1)))

    def return_dice(self, dice: Dice) -> None:
        """Return dice to the dice pool.

        :param dice: Dice to return to the dice pool.
        """
        self.dice_pool.append(dice)

    def shuffle_dice_pool(self) -> None:
        """Shuffle dices in the dice pool.
        """
        shuffle(self.dice_pool)

    def create_dices(self) -> None:
        """Create dices and fill the dice pool.
        """
        self.dice_pool.clear()
        for dice_type in DICES:
            # Create dices of each color
            for i in range(DICES[dice_type].amount):
                dice = Dice(dice_type)
                self.dice_pool.append(dice)

        self.shuffle_dice_pool()  # Shuffle dices in dice pool

    def display_dices(self) -> None:
        """Show dices in the dice pool.
        """
        print(Strings.display_dices(self.dice_pool))

    def setup_game(self) -> None:
        """Setup game, players and dices.
        """
        clear_console()
        print(Strings.greet_user())  # Greet user
        self.create_dices()  # Create dices
        self.create_players()   # Create players
        self.state = GameStates.GAME  # Change state to GAME

    def create_players(self) -> None:
        """Ask players names, create and store them.
        """
        number_of_players = int_input(Strings.ask_num_players, MIN_PLAYERS, MAX_PLAYERS)  # Ask number of players
        for player in range(number_of_players):
            player_name = text_input(Strings.ask_name)
            new_player = Player(player_name, self)
            self.players.append(new_player)

    def end_game(self) -> None:
        """End game. Show players score and congrats winner.
        """
        print(Strings.end_game_players(self.players, self.winners[0].name))
        input(Strings.end_game)
        clear_console()
        answer = bool_input(Strings.ask_continue)  # Ask if user wants to play again
        if answer:
            self.reset_game()  # Set game for next play
        else:
            quit()  # Exit game

    def reset_game(self) -> None:
        """Reset game memory back to initialization.
        """
        self.players.clear()
        self.dice_pool.clear()
        self.winners.clear()
        self.highest_score = 0
        self.state = GameStates.SETUP

    def game_round(self, players: list[Player]) -> None:
        """Run a game turn, looping through all players.
        """
        for player in players:
            player.turn()  # Player turn
            if player.score > self.highest_score:
                self.highest_score = player.score  # Update the highest score in the game

        # Check if someone wins or if it's a draw
        self.winners.clear()
        if self.highest_score >= SCORE_LIMIT:
            for player in players:
                if player.score == self.highest_score:
                    self.winners.append(player)  # Save each player that reached the highest score
                    self.state = GameStates.DRAW
        if self.winners and len(self.winners) < 2:
            # There is only one player with the highest score
            self.state = GameStates.END
        else:
            print(Strings.draw(self.winners))  # Inform the user there is a draw

    def game_loop(self) -> None:
        """All the game happens inside this loop.
        It controls the flow of the game.
        """
        while True:
            match self.state:
                case GameStates.SETUP:
                    self.setup_game()  # Set the game up
                case GameStates.GAME:
                    self.game_round(self.players)  # Game turn with all players
                case GameStates.DRAW:
                    self.game_round(self.winners)  # Game turn with draw players
                case GameStates.END:
                    self.end_game()  # End the game
