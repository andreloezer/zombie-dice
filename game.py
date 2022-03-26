"""

    All the game logic

"""


from random import randint, shuffle


from dice import Dice
from player import Player
from strings import GameStrings as Strings
from config import DICES, SCORE_LIMIT, MIN_PLAYERS, MAX_PLAYERS
from utils import int_input, text_input, bool_input, clear_console


# Store game states
class GameStates:
    SETUP = "setup"
    GAME = "game"
    DRAW = "draw"
    END = "end"


# All the Game logic
class Game:
    def __init__(self):
        self.players = []
        self.dice_pool = []
        self.winners = []
        self.highest_score = 0
        self.state = GameStates.SETUP
        self.game_loop()

    # Give 1 dice to the player
    def take_dice(self):
        return self.dice_pool.pop(randint(0, (len(self.dice_pool) - 1)))

    # Create dices
    def create_dices(self):
        self.dice_pool.clear()
        for dice_type in DICES:
            # Create dices of each color
            for i in range(DICES[dice_type]):
                dice = Dice(dice_type)
                self.dice_pool.append(dice)
        shuffle(self.dice_pool)

    # Show dices in the dice pool
    def display_dices(self):
        print(Strings.display_dices(self.dice_pool))

    # Setup game, players and dices
    def setup_game(self):
        # Greet user
        clear_console()
        print(Strings.greet_user())

        # Create dices
        self.create_dices()

        # Create players
        self.create_players()

        # Change state to GAME
        self.state = GameStates.GAME

    # Create players
    def create_players(self):
        # Ask number of players
        number_of_players = int_input(Strings.ask_num_players, MIN_PLAYERS, MAX_PLAYERS)
        for player in range(number_of_players):
            player_name = text_input(Strings.ask_name)
            new_player = Player(player_name, self)
            self.players.append(new_player)

    # End game: Show players score and congrats winner
    def end_game(self):
        print(Strings.end_game_players(self.players, self.winners[0].name))
        input(Strings.end_game)
        clear_console()
        # Ask if user wants to play again
        answer = bool_input(Strings.ask_continue)
        if answer:
            # Set game for next play
            self.reset_game()
        else:
            # Exit game
            quit()

    # Reset game memory back to initialization
    def reset_game(self):
        self.players.clear()
        self.dice_pool.clear()
        self.winners.clear()
        self.highest_score = 0
        self.state = GameStates.SETUP

    # Run a game turn
    def game_turn(self, players):
        for player in players:
            # Player round
            player.round()
            if player.score > self.highest_score:
                # Update the highest score in the game
                self.highest_score = player.score

        # Check if someone wins or if it's a draw
        self.winners.clear()
        if self.highest_score >= SCORE_LIMIT:
            for player in players:
                if player.score == self.highest_score:
                    # Save each player that reached the highest score
                    self.winners.append(player)
                    self.state = GameStates.DRAW
        if self.winners and len(self.winners) < 2:
            # There is only one player with the highest score
            self.state = GameStates.END
        else:
            # Inform the user there is a draw
            print(Strings.draw(self.winners))

    # All the Game happens inside this loop
    def game_loop(self):
        while True:
            match self.state:
                case GameStates.SETUP:
                    # Set the game up
                    self.setup_game()
                case GameStates.GAME:
                    # Game turn with all players
                    self.game_turn(self.players)
                case GameStates.DRAW:
                    # Game turn with draw players
                    self.game_turn(self.winners)
                case GameStates.END:
                    # End the game
                    self.end_game()
