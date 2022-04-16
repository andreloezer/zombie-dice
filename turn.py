"""Turn class, controls turn actions
"""


import game
from player import Player
from dice import Dice
from config import BRAIN, RUN, SHOTGUN, SHOTS_LIMIT, DICES_PER_ROUND
from strings import TurnStrings as Strings
from utils import clear_console, stringify


class _TurnStates:
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
        self.__game = game_ref
        self.__player = player_ref
        self.__round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }
        self.__amount_picked_dices = 0
        self.__hand_dices: list[Dice] = []
        self.__table_dices: list[Dice] = []
        self.__get_dices_amount = DICES_PER_ROUND
        self.__state = _TurnStates.GAME
        self.__turn()

    def __str__(self) -> str:
        """Return a string representing the current player turn with all the relevant information.

        :return: String representing the player turn.
        """
        return Strings.display_turn(self.__player.index + 1,
                                    self.__player.name,
                                    self.__round_status,
                                    self.__amount_picked_dices,
                                    self.__player.score)

    def __turn(self) -> None:
        """Control all the player actions in the turn through a loop using state.
        """
        self.state = _TurnStates.GAME
        while True:
            match self.__state:
                case _TurnStates.GAME:
                    self.__play()  # Play a turn
                case _TurnStates.END:
                    self.__end_round()  # End player turn saving score
                case _TurnStates.LOST:
                    self.__lost()  # End player turn not saving score
                case _TurnStates.EXIT:
                    return

    def __play(self) -> None:
        """Play one hand.
        """
        # Inform the player it's their turn
        clear_console()
        print(Strings.enter_turn(self.__game.round_count,
                                 self.__player.index + 1,
                                 self.__player.name,
                                 self.__player.score,
                                 self.__round_status[BRAIN]))
        self.__get_dices()  # Get dices
        self.__roll_dices()  # Roll dices in hand

        # Check if player lost the turn
        if self.__round_status[SHOTGUN] >= SHOTS_LIMIT:
            self.__state = _TurnStates.LOST
            return

        # Calculate how many dices to get from the pool on the next turn
        self.__get_dices_amount = DICES_PER_ROUND - self.__round_status[RUN]
        print(self)  # Show player current turn status

        self.__ask_continue()  # Ask if player wants to continue playing the turn

        if len(self.__game.dice_pool) < self.__get_dices_amount:
            # Not enough dices to continue the player turn
            self.__continue_playing()

    def __get_dices(self) -> None:
        """Get dices from dice pool and store them in the hand.
        """
        # Skip if player already have sufficient dices in hand to roll
        if self.__get_dices_amount == 0:
            return

        self.__game.shuffle_dice_pool()  # Shuffle dices before picking
        self.__game.display_dices()  # Show available dices in the pool
        input(Strings.ask_pick_dices(self.__get_dices_amount))  # Ask player to pick the dices

        # Pick and display dices to the player
        self.__amount_picked_dices += self.__get_dices_amount
        picked_dices = []
        for i in range(self.__get_dices_amount):
            dice = self.__game.take_dice()
            picked_dices.append(dice)
        print(Strings.picked_dices(stringify(picked_dices)))
        self.__hand_dices.extend(picked_dices)

    def __roll_dices(self) -> None:
        """Roll dices in hand, randomly choosing a side for each.
        """
        self.__round_status[RUN] = 0  # Reset previous RUN dices count
        input(Strings.ask_throw_dices)  # Ask player to roll the dices

        # Roll all dices in hand
        for dice in self.__hand_dices:
            dice.roll_dice()
            self.__round_status[dice.value] += 1  # Save result player score

        print(Strings.rolled_dices(stringify(self.__hand_dices)))
        input(Strings.prompt_continue)

    def __ask_continue(self) -> None:
        """Ask if player wants to continue playing more hands in the current turn.
        """
        answer = self.__player.ask_continue(self.__get_dices_amount)
        if answer:
            self.__clear_hand_dices()  # Clear hand dices for next throw
        else:
            self.__state = _TurnStates.END

    def __continue_playing(self) -> None:
        """Return all BRAIN dices to the pool to keep playing.
        """
        print(Strings.picked_all_dices)
        for dice in self.__table_dices:
            if dice.value == BRAIN:
                dice.reset_side()
                self.__game.return_dice(dice)

    def __clear_hand_dices(self) -> None:
        """Remove all dices that aren't RUN from the hand, preparing for the next throw.
        """
        hand_copy = self.__hand_dices.copy()
        for dice in hand_copy:
            if not dice.value == RUN:
                self.__table_dices.append(dice)
                self.__hand_dices.remove(dice)

    def __end_round(self) -> None:
        """Finish the turn and update player score.
        """
        self.__player.score += self.__round_status[BRAIN]
        self.__state = _TurnStates.EXIT  # Update turn state to exit
        input(Strings.prompt_continue)

    def __lost(self) -> None:
        """Player looses the score accumulated in the turn.
        Inform the loss and proceed to the next player turn or game round.
        """
        print(self)
        print(Strings.round_lost(self.__player.index + 1, self.__player.name, self.__round_status[SHOTGUN]))
        input(Strings.prompt_continue)
        self.__state = _TurnStates.EXIT
