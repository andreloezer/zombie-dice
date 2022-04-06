"""Text, and it's logics, printed or prompted to the user/player.
"""


from style import BOLD, UND, style_text as style
from config import RED, GREEN, BRAIN, SHOTGUN, SHOTS_LIMIT, DICES, SCORE_LIMIT, DICES_PER_ROUND, RUN,\
                   TERMINAL_WIDTH, MAX_PLAYERS, MIN_PLAYERS
from math import floor


# Game name
GAME_NAME = "Bem vindo ao ZOMBIE DICE!!!"
# Indent for text print
INDENT = " " * 4


# Strings for the Game class
class GameStrings:
    """Class to store all Game class related strings that interface with the user.
    """
    ask_num_players = f"Quantas pessoas vão jogar? ({MIN_PLAYERS}, {MAX_PLAYERS}): "
    end_game = "\nPressione ENTER para encerrar..."
    ask_continue = "Jogar mais uma vez? "

    @staticmethod
    def greet_user():
        text = (f"{'=' * TERMINAL_WIDTH}\n\n{' ' * int(floor(TERMINAL_WIDTH - len(GAME_NAME)) / 2)}"
                f"{style(GAME_NAME, BOLD)}\n\n"
                f"{'=' * TERMINAL_WIDTH}\n"
                f"\nO {style('Zombie Dice', BOLD)} é um jogo de dados onde o jogador é um zumbi que precisa comer "
                f"{style(BRAIN.capitalize(), BOLD)} para vencer!\n\n"
                f"O jogo possui {style(sum([dice.amount for dice in DICES.values()]), BOLD, UND)} dados, "
                f"sendo que cada um representa uma vítima.\n"
                f"Existem {style(len(DICES), BOLD, UND)} tipos de dados, cada um com um nível de dificuldade:\n")
        for dice_type in DICES:
            text += f"\n{INDENT}{style(dice_type.capitalize(), BOLD, dice_type) + ':':26}"
            for side in DICES[dice_type].sides:
                text += f" {style(side.capitalize(), BOLD):18}"
        text += (
            f"\n\nGanha o jogo quem conseguir comer "
            f"{style(SCORE_LIMIT, BOLD, UND)} {style(BRAIN.capitalize(), BOLD)}.\n"
            f"Ao rolar os {style(DICES_PER_ROUND, BOLD, UND)} "
            f"dados o jogador pode escolher encerrar o turno, ou continuar rolando.\n"
            f"Para continuar é preciso atender aos seguintes critérios:\n"
            f"{INDENT}- O jogador não pode ter acumulado {style(SHOTS_LIMIT, BOLD, UND)} "
            f"ou mais {style(SHOTGUN.capitalize(), BOLD)};\n"
            f"{INDENT}- Os dados que deram {style(RUN.capitalize(), BOLD)} deveram ser re-rolados;\n"
            f"{INDENT}- É necessário que ainda tenha no pote dados suficientes para pegar e rolar mais "
            f"{style(DICES_PER_ROUND, BOLD, UND)} dados;\n"
            f"\nMesmo que um jogador atinja a condição de vitória, "
            f"todos os jogadores restantes na rodada tem o direito de jogar também.\n"
            f"Caso 2 ou mais jogadores atinjam uma mesma pontuação igual ou acima da condição de vitória, "
            f"haverá uma rodada de desempate até que sobre apenas 1 jogador com uma pontuação máxima.\n"
        )
        text += f"\n{'=' * TERMINAL_WIDTH}\n"
        return text

    @staticmethod
    def display_dices(dices):
        text = "\nDados disponíveis no pote:"
        for dice in dices:
            text += f"\n{INDENT}{dice}"

        text += "\n\nO pote contém os seguintes tipos de dados:"
        for color in DICES.keys():
            amount = len([dice for dice in dices if dice.color == color])
            text += f"\n{INDENT}{style(color.capitalize(), BOLD, color) + ':':23} {style(amount, BOLD)}"

        return text

    @staticmethod
    def draw(players):
        text = "\nOs seguintes jogadores empataram:\n"
        for player in players:
            text += f"{INDENT}{player}"
        return text

    @staticmethod
    def end_game_players(players, winner):
        text = "\nPontuação final de cada jogador:\n"
        for player in players:
            text += f"{INDENT}{player}\n"
        text += f"\nParabéns {style(winner, BOLD, UND)}, você ganhou!!!"
        return text


# Strings for the Player class
class TurnStrings:
    """Class to store all Player class related strings to be printed that interface with the user.
    """
    ask_throw_dices = "\nPressione ENTER para jogar os dados..."
    prompt_continue = "\nPressione ENTER para continuar..."
    picked_all_dices = (f"Não há mais dados suficientes no tubo para mais uma rodada. Os dados que deram "
                        f"{style(BRAIN, BOLD, UND)} serão re-colocados no tubo para continuar o seu turno.")

    @staticmethod
    def picked_dices(dices):
        text = "\nDados pegos do pote:"
        for dice in dices:
            text += f"\n{INDENT}{dice}"
        return text

    @staticmethod
    def rolled_dices(dices):
        text = "\nDados rolados:"
        for dice in dices:
            text += f"\n{INDENT}{dice}"
        return text

    @staticmethod
    def repr(name, stats, dices, score):
        text = f"\nDados acumulados pelo jogador {style(name, BOLD, UND)} nesse turno:\n"
        for stat in stats:
            text += f"{INDENT}{(style(f'{stat.capitalize()}:', BOLD)):20}{style(stats[stat], BOLD)}\n"
        text += (f"\nVocê já acumulou {style(stats[BRAIN], GREEN, BOLD, UND)} ponto(s) nessa rodada e "
                 f"{style(score + stats[BRAIN], BOLD, UND)} no total.\n"
                 f"Você já pegou {style(dices, BOLD, UND)} dados neste turno.")
        if stats[SHOTGUN] == 2:
            text += (f"\nCuidado, você já tomou {style(stats[SHOTGUN], RED, BOLD, UND)} tiros nessa rodada, "
                     f"o limite é de {style(SHOTS_LIMIT, BOLD, UND)} tiros!")
        return text

    @staticmethod
    def enter_turn(name, score, current):
        return (f"\n{'=' * TERMINAL_WIDTH}\nTurno do(a) {style(name, BOLD, UND)}"
                f", a sua pontuação atual é de {style(score, GREEN, BOLD, UND)}"
                f" pontos, o seu acumulado é {style(score + current, GREEN, BOLD, UND)} pontos;")

    @staticmethod
    def round_lost(name, shots):
        return f"\nO jogador {style(name, BOLD, UND)} acumulou "\
               f"{style(shots, RED, BOLD, UND)} tiros e perdeu o turno!"

    @staticmethod
    def ask_pick_dices(amount):
        return f"\nPressione ENTER para pegar {style(amount, BOLD, UND)} dados do pote..."


# Strings for the Player class
class PlayerStrings:
    """Class to store all Player class related strings to be printed that interface with the user.
    """
    ask_name = "Nome do jogador: "

    @staticmethod
    def repr_player(name, score):
        return f"{style(name, BOLD, UND)} fez {style(score, BOLD)} pontos."

    @staticmethod
    def ask_continue(dices):
        return f"\nPegar mais {style(dices, BOLD, UND)} dados e continuar jogando ou passar a vez? (s/n)"


# Strings for the Dice class
class DiceStrings:
    """Class to store all Dice class related strings to be printed that interface with the user.
    """
    @staticmethod
    def repr(color, value):
        if not value:
            return f"Dado: {style(color.capitalize(), color)}"
        return f"Dado: {style(color.capitalize(), color):20}Lado: {style(value.capitalize(), BOLD)}"


# Strings for the Utils functions
class UtilsStrings:
    """Class to store all the utils functions strings that interface with the user.
    """
    str_warning = "Por favor entre uma resposta válida.\n"
    truthy = ("s",)
    falsy = ("n",)
    bool_warning = "Resposta invalida, por favor escreva sim ou não."

    @staticmethod
    def int_warning(min_val, max_val):
        return f"Por favor entre com um número inteiro entre {min_val} e {max_val}.\n"
