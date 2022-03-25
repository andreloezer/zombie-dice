"""

    Game configurations, settings, and other constants

"""


import os


# General settings
SCORE_LIMIT = 13
SHOTS_LIMIT = 3
DICES_PER_ROUND = 3
MIN_PLAYERS = 2
MAX_PLAYERS = 99


# Colors
RED = "vermelho"
YELLOW = "amarelo"
GREEN = "verde"


# Dice sides
BRAIN = "cérebros"
RUN = "passos"
SHOTGUN = "tiros"


# Dices sides
DICE_TYPES = {
    RED: (BRAIN, RUN, RUN, SHOTGUN, SHOTGUN, SHOTGUN),
    YELLOW: (BRAIN, BRAIN, RUN, RUN, SHOTGUN, SHOTGUN),
    GREEN: (BRAIN, BRAIN, BRAIN, RUN, RUN, SHOTGUN)
}


# Dices amount
DICES = {
    RED: 3,
    YELLOW: 4,
    GREEN: 6
}


# Environment settings
USE_STYLES = True
OS = os.name
TERMINAL_WIDTH = os.get_terminal_size().columns
