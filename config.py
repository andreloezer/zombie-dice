"""Game configurations, settings, and other constants."""


import os
from dataclasses import dataclass


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


@dataclass
class DiceType:
    sides: tuple
    amount: int


# Dices configuration
DICES: dict[str, DiceType] = {
    RED: DiceType((BRAIN, RUN, RUN, SHOTGUN, SHOTGUN, SHOTGUN), 3),
    YELLOW: DiceType((BRAIN, BRAIN, RUN, RUN, SHOTGUN, SHOTGUN), 4),
    GREEN: DiceType((BRAIN, BRAIN, BRAIN, RUN, RUN, SHOTGUN), 6),
}


# Environment settings
USE_STYLES = True
OS = os.name
TERMINAL_WIDTH = os.get_terminal_size().columns
