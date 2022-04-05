"""Player class and related logic.
"""


import game
from dice import Dice
from strings import PlayerStrings as Strings
from utils import bool_input, clear_console, text_input
from config import BRAIN, RUN, SHOTGUN, SHOTS_LIMIT, DICES_PER_ROUND


class PlayerStates:
    """Class to store player states.
    """
    GAME = "game"
    END = "end"
    LOST = "lost"
    EXIT = "exit"


class Player:
    """Class representing the player.

    :param game_ref: Reference to the game instance.
    """

    # Solution to avoid circular imports when adding type annotations:
    # https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports/39757388#39757388
    # https://peps.python.org/pep-0484/#forward-references
    def __init__(self, game_ref: "game.Game") -> None:
        """Init player.

        :param game_ref: Reference to the game instance.
        """
        self.game = game_ref
        self.name = self.ask_name()
        self.score = 0
        self.round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }
        self.dices = 0
        self.hand_dices: list[Dice] = []
        self.table_dices: list[Dice] = []
        self.get_dices_amount = DICES_PER_ROUND
        self.state = PlayerStates.GAME

    def __repr__(self) -> str:
        """Return a string representing the player with its name and score.
        """
        return Strings.repr_player(self.name, self.score)

    @staticmethod
    def ask_name() -> str:
        return text_input(Strings.ask_name)

    def clear_hand_dices(self) -> None:
        """Remove all dices that aren't RUN from player hand preparing for the next throw.
        """
        hand_copy = self.hand_dices.copy()
        for dice in hand_copy:
            if not dice.side == RUN:
                self.table_dices.append(dice)
                self.hand_dices.remove(dice)

    def player_reset(self) -> None:
        """Reset game dice pool and player status.
        """
        # Reset dices
        self.hand_dices.clear()
        self.game.create_dices()
        self.dices = 0
        self.get_dices_amount = DICES_PER_ROUND

        # Reset turn status
        self.round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }

    def get_dices(self) -> None:
        """Get dices from dice pool and store them in the player hand.
        """
        # Skip if player already have sufficient dices in hand to roll
        if self.get_dices_amount == 0:
            return

        self.game.shuffle_dice_pool()  # Shuffle dices before picking
        self.game.display_dices()  # Show available dices in the pool
        input(Strings.ask_pick_dices(self.get_dices_amount))  # Ask player to pick the dices

        # Pick and display dices to the player
        self.dices += self.get_dices_amount
        picked_dices = []
        for i in range(self.get_dices_amount):
            dice = self.game.take_dice()
            picked_dices.append(dice)
        print(Strings.picked_dices(picked_dices))
        self.hand_dices.extend(picked_dices)

    def roll_dices(self) -> None:
        """Roll dices in hand, randomly choosing a side for each.
        """
        self.round_status[RUN] = 0  # Reset previous RUN dices count
        input(Strings.ask_throw_dices)  # Ask player to roll the dices

        # Roll all dices in hand
        for dice in self.hand_dices:
            dice.roll_dice()
            self.round_status[dice.side] += 1  # Save result player score

        print(Strings.rolled_dices(self.hand_dices))
        input(Strings.prompt_continue)

    # Show player current turn status
    def print_stats(self) -> None:
        """Print player current turn info."""
        print(Strings.stats(self.round_status,
                            self.dices,
                            self.score + self.round_status[BRAIN]))

    def turn(self) -> None:
        """Control all the player actions in the turn through a loop using state.
        """
        self.state = PlayerStates.GAME
        while True:
            match self.state:
                case PlayerStates.GAME:
                    self.play()  # Play a turn
                case PlayerStates.END:
                    self.end_round()  # End player turn saving score
                case PlayerStates.LOST:
                    self.lost()  # End player turn not saving score
                case PlayerStates.EXIT:
                    self.player_reset()  # Clear player turn info and exit turn loop
                    return

    def play(self) -> None:
        """Play one hand.
        """
        # Inform the player it's their turn
        clear_console()
        print(Strings.enter_round(self.name, self.score, self.round_status[BRAIN]))
        self.get_dices()  # Get dices
        self.roll_dices()  # Roll dices in hand

        # Check if player lost the turn
        if self.round_status[SHOTGUN] >= SHOTS_LIMIT:
            self.state = PlayerStates.LOST
            return

        # Calculate how many dices to get from the pool on the next turn
        self.get_dices_amount = DICES_PER_ROUND - self.round_status[RUN]
        self.print_stats()  # Show player current turn status

        self.ask_continue()  # Ask if player wants to continue playing the turn

        if len(self.game.dice_pool) < self.get_dices_amount:
            # Not enough dices to continue the player turn
            self.continue_playing()

    def continue_playing(self) -> None:
        """Return all BRAIN dices to the pool to keep playing.
        """
        print(Strings.picked_all_dices)
        for dice in self.table_dices:
            if dice.side == BRAIN:
                dice.reset_side()
                self.game.return_dice(dice)

    def ask_continue(self) -> None:
        """Ask if player wants to continue playing more hands in the current turn.
        """
        answer = bool_input(Strings.ask_continue(self.get_dices_amount))
        if answer:
            self.clear_hand_dices()  # Clear hand dices for next throw
        else:
            self.state = PlayerStates.END

    def lost(self) -> None:
        """Player looses the score accumulated in the turn.
        Inform the loss and reset player.
        """
        self.print_stats()
        print(Strings.round_lost(SHOTS_LIMIT))
        input(Strings.prompt_continue)
        self.state = PlayerStates.EXIT

    def end_round(self) -> None:
        """Finish the turn and update player score.
        """
        self.score += self.round_status[BRAIN]
        self.state = PlayerStates.EXIT  # Update player state to exit
        input(Strings.prompt_continue)
