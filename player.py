"""

    All the player logic

"""


from strings import PlayerStrings as Strings
from utils import bool_input, clear_console
from config import BRAIN, RUN, SHOTGUN, SHOTS_LIMIT, DICES_PER_ROUND


# Store player states
class PlayerStates:
    GAME = "game"
    END = "end"
    LOST = "lost"
    EXIT = "exit"


# All the Player logic
class Player:
    def __init__(self, name, game_ref):
        self.name = name
        self.game = game_ref
        self.score = 0
        self.round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }
        self.dices = 0
        self.hand_dices = []
        self.get_dices_amount = DICES_PER_ROUND
        self.state = PlayerStates.GAME

    # Return player string
    def __repr__(self):
        return Strings.repr_player(self.name, self.score)

    # Clear hand of not RUN dices to the next throw
    def clear_hand_dices(self):
        # Remove all dices with side not equal to RUN
        hand_copy = self.hand_dices.copy()
        for dice in hand_copy:
            if not dice.side == RUN:
                self.hand_dices.remove(dice)

    # Return dices to pool
    def player_reset(self):
        # Reset dices
        self.hand_dices.clear()
        self.game.create_dices()
        self.dices = 0
        self.get_dices_amount = DICES_PER_ROUND

        # Reset round status
        self.round_status = {
            BRAIN: 0,
            RUN: 0,
            SHOTGUN: 0
        }

    # Get dices from dice pool
    def get_dices(self):
        # Skip if player already have sufficient dices in hand to roll
        if self.get_dices_amount == 0:
            return

        # Show available dices in the pool
        self.game.display_dices()

        # Ask player to pick the dices
        input(Strings.ask_pick_dices(self.get_dices_amount))

        # Pick and display dices to the player
        self.dices += self.get_dices_amount
        picked_dices = []
        for i in range(self.get_dices_amount):
            dice = self.game.take_dice()
            picked_dices.append(dice)
        print(Strings.picked_dices(picked_dices))
        self.hand_dices.extend(picked_dices)

    # Roll dices in hand
    def roll_dices(self):
        # Reset previous RUN dices count
        self.round_status[RUN] = 0
        # Ask player to roll the dices
        input(Strings.ask_throw_dices)
        # Roll all dices in hand
        for dice in self.hand_dices:
            dice.roll_dice()
            # Save result player score
            self.round_status[dice.side] += 1
        print(Strings.rolled_dices(self.hand_dices))
        input(Strings.prompt_continue)

    # Show player current round status
    def print_stats(self):
        print(Strings.stats(self.round_status,
                            self.dices,
                            self.score + self.round_status[BRAIN]))

    # All the Player actions through the round is done in this loop
    def round(self):
        # Control the player actions
        self.state = PlayerStates.GAME
        while True:
            match self.state:
                case PlayerStates.GAME:
                    # Play a round
                    self.play()
                case PlayerStates.END:
                    # End player round saving score
                    self.end_round()
                case PlayerStates.LOST:
                    # End player round not saving score
                    self.lost()
                case PlayerStates.EXIT:
                    # Clear player round info and exit round loop
                    self.player_reset()
                    return

    # Play one roll
    def play(self):
        # Inform the player it's their round
        clear_console()
        print(Strings.enter_round(self.name, self.score, self.round_status[BRAIN]))
        # Get dices
        self.get_dices()

        # Roll dices in hand
        self.roll_dices()

        # Check if player lost round
        if self.round_status[SHOTGUN] >= SHOTS_LIMIT:
            self.state = PlayerStates.LOST
            return

        # Calculate how many dices to get from the pool on the next round
        self.get_dices_amount = DICES_PER_ROUND - self.round_status[RUN]

        # Show player current round status
        self.print_stats()

        if len(self.game.dice_pool) < self.get_dices_amount:
            # Not enough dices to continue the player round
            print(Strings.picked_all_dices)
            self.state = PlayerStates.END
            return

        # Ask if player wants to continue playing the round
        self.ask_continue()

    # Ask if the player wants to continue throwing more dices
    def ask_continue(self):
        answer = bool_input(Strings.ask_continue(self.get_dices_amount))
        if answer:
            # Clear hand dices for next throw
            self.clear_hand_dices()
        else:
            self.state = PlayerStates.END

    # Inform the loss and reset player
    def lost(self):
        self.print_stats()
        print(Strings.round_lost(SHOTS_LIMIT))
        input(Strings.prompt_continue)
        self.state = PlayerStates.EXIT

    # Account round score
    def end_round(self):
        self.score += self.round_status[BRAIN]
        # Update game state to exit
        self.state = PlayerStates.EXIT
        input(Strings.prompt_continue)
