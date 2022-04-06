"""Turn class, controls turn actions
"""


import game
from player import Player
from dice import Dice
from config import BRAIN, RUN, SHOTGUN, SHOTS_LIMIT, DICES_PER_ROUND
from strings import TurnStrings as Strings
from utils import clear_console


class TurnStates:
    """Class to store turn states
    """
    GAME = "game"
    END = "end"
    LOST = "lost"
    EXIT = "exit"


class Turn:
    """Class representing the turn.

    :param game_ref: Reference to the game instance.
    :param player_ref: Reference to the current player instance.
    """

    # Solution to avoid circular imports when adding type annotations:
    # https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports/39757388#39757388
    # https://peps.python.org/pep-0484/#forward-references
    def __init__(self, game_ref: "game.Game", player_ref: Player) -> None:
        self.game = game_ref
        self.player = player_ref
        self.round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }
        self.dices = 0
        self.hand_dices: list[Dice] = []
        self.table_dices: list[Dice] = []
        self.get_dices_amount = DICES_PER_ROUND
        self.state = TurnStates.GAME
        self.turn()

    def __repr__(self) -> str:
        """Return a string representing the current player turn with all the relevant information.

        :return: String representing the player turn.
        """
        return Strings.repr(self.player.name,
                            self.round_status,
                            self.dices,
                            self.player.score)

    def turn(self) -> None:
        """Control all the player actions in the turn through a loop using state.
        """
        self.state = TurnStates.GAME
        while True:
            match self.state:
                case TurnStates.GAME:
                    self.play()  # Play a turn
                case TurnStates.END:
                    self.end_round()  # End player turn saving score
                case TurnStates.LOST:
                    self.lost()  # End player turn not saving score
                case TurnStates.EXIT:
                    return

    def play(self) -> None:
        """Play one hand.
        """
        # Inform the player it's their turn
        clear_console()
        print(Strings.enter_turn(self.game.round_count,
                                 self.player.name,
                                 self.player.score,
                                 self.round_status[BRAIN]))
        self.get_dices()  # Get dices
        self.roll_dices()  # Roll dices in hand

        # Check if player lost the turn
        if self.round_status[SHOTGUN] >= SHOTS_LIMIT:
            self.state = TurnStates.LOST
            return

        # Calculate how many dices to get from the pool on the next turn
        self.get_dices_amount = DICES_PER_ROUND - self.round_status[RUN]
        print(self)  # Show player current turn status

        self.ask_continue()  # Ask if player wants to continue playing the turn

        if len(self.game.dice_pool) < self.get_dices_amount:
            # Not enough dices to continue the player turn
            self.continue_playing()

    def get_dices(self) -> None:
        """Get dices from dice pool and store them in the hand.
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

    def ask_continue(self) -> None:
        """Ask if player wants to continue playing more hands in the current turn.
        """
        answer = self.player.ask_continue(self.get_dices_amount)
        if answer:
            self.clear_hand_dices()  # Clear hand dices for next throw
        else:
            self.state = TurnStates.END

    def continue_playing(self) -> None:
        """Return all BRAIN dices to the pool to keep playing.
        """
        print(Strings.picked_all_dices)
        for dice in self.table_dices:
            if dice.side == BRAIN:
                dice.reset_side()
                self.game.return_dice(dice)

    def clear_hand_dices(self) -> None:
        """Remove all dices that aren't RUN from player hand preparing for the next throw.
        """
        hand_copy = self.hand_dices.copy()
        for dice in hand_copy:
            if not dice.side == RUN:
                self.table_dices.append(dice)
                self.hand_dices.remove(dice)

    def end_round(self) -> None:
        """Finish the turn and update player score.
        """
        self.player.score += self.round_status[BRAIN]
        self.state = TurnStates.EXIT  # Update turn state to exit
        input(Strings.prompt_continue)

    def lost(self) -> None:
        """Player looses the score accumulated in the turn.
        Inform the loss and proceed to the next player turn or game round.
        """
        print(self)
        print(Strings.round_lost(self.player.name, self.round_status[SHOTGUN]))
        input(Strings.prompt_continue)
        self.state = TurnStates.EXIT
