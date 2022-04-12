"""Text, and it's logics, printed or prompted to the user/player.
"""


from math import floor

from style import BOLD, UND, style_text as style
from config import RED, GREEN, BRAIN, SHOTGUN, SHOTS_LIMIT, DICES, SCORE_LIMIT, DICES_PER_ROUND, RUN,\
                   TERMINAL_WIDTH, MAX_PLAYERS, MIN_PLAYERS
import dice

# Game name
GAME_NAME = "Bem vindo ao ZOMBIE DICE!!!"
# Indent for text print
INDENT = " " * 4


class GameStrings:
    """Class to store all Game class related strings that interface with the user.
    """
    ask_num_players = f"Quantas pessoas vão jogar? ({MIN_PLAYERS}, {MAX_PLAYERS}): "
    end_game = "\nPressione ENTER para encerrar..."
    ask_continue = "Jogar mais uma vez? "

    @staticmethod
    def greet_user() -> str:
        """Greet user by present the game showing its name, the rules and explaining how it works.

        :return: String presenting the game and explaining its rules.
        """
        text = (f"{'=' * TERMINAL_WIDTH}\n\n{' ' * int(floor(TERMINAL_WIDTH - len(GAME_NAME)) / 2)}"
                f"{style(GAME_NAME, BOLD)}\n\n"
                f"{'=' * TERMINAL_WIDTH}\n"
                f"\nO {style('Zombie Dice', BOLD)} é um jogo de dados onde o jogador é um zumbi que precisa comer "
                f"{style(BRAIN.capitalize(), BOLD)} para vencer!\n\n"
                f"O jogo possui {style(sum([dice_obj.amount for dice_obj in DICES.values()]), BOLD, UND)} dados, "
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
            f"Para continuar jogando o turno é preciso atender aos seguintes critérios:\n"
            f"{INDENT}- O jogador não pode ter acumulado {style(SHOTS_LIMIT, BOLD, UND)} "
            f"ou mais {style(SHOTGUN.capitalize(), BOLD)};\n"
            f"{INDENT}- Os dados que deram {style(RUN.capitalize(), BOLD)} deverão ser re-rolados;\n"
            f"{INDENT}- Caso não haja mais dados suficientes no pote para pegar e rolar mais "
            f"{style(DICES_PER_ROUND, BOLD, UND)}, os dados que deram "
            f"{style(BRAIN.capitalize(), BOLD)} serão re-colocados no pote e o turno continuará;\n"
            f"\nMesmo que um jogador atinja a condição de vitória, "
            f"todos os jogadores restantes na rodada tem o direito de jogar também.\n"
            f"Caso 2 ou mais jogadores atinjam uma mesma pontuação igual ou acima da condição de vitória, "
            f"haverá uma rodada de desempate até que sobre apenas 1 jogador com uma pontuação máxima.\n"
        )
        text += f"\n{'=' * TERMINAL_WIDTH}\n"
        return text

    @staticmethod
    def display_dices(dices: list["dice.Dice"]) -> str:
        """Display all dices available in the dice pool for the player to pick.

        :param dices: List of dices
        :return: String showing all dices available in the dice pool.
        """
        text = "\nDados disponíveis no pote:"
        for dice_obj in dices:
            text += f"\n{INDENT}{dice_obj}"

        text += "\n\nO pote contém os seguintes tipos de dados:"
        for color in DICES.keys():
            amount = len([dice for dice_obj in dices if dice_obj.color == color])
            text += f"\n{INDENT}{style(color.capitalize(), BOLD, color) + ':':23} {style(amount, BOLD)}"

        return text

    @staticmethod
    def draw(players: list[str]) -> str:
        """Show players that have tied in the game.

        :param players: List of tied players.
        :return: String showing tied players.
        """
        text = "\nOs seguintes jogadores empataram:\n"
        for player in players:
            text += f"{INDENT}{player}"
        return text

    @staticmethod
    def end_game_players(players: list[str], winner: list[str]) -> str:

        """Show all players final score and congratulates the winner.

        :param players: List of all the players of the game.
        :param winner: Player winner of the game.
        :return: String showing all players final score and congratulating the winner.
        """
        text = "\nPontuação final de cada jogador:\n"
        for player in players:
            text += f"{INDENT}{player}\n"
        text += f"\nParabéns {style(winner, BOLD, UND)}, você ganhou!!!"
        return text


class TurnStrings:
    """Class to store all Player class related strings to be printed that interface with the user.
    """
    ask_throw_dices = "\nPressione ENTER para jogar os dados..."
    prompt_continue = "\nPressione ENTER para continuar..."
    picked_all_dices = (f"Não há mais dados suficientes no tubo para mais uma rodada. Os dados que deram "
                        f"{style(BRAIN, BOLD, UND)} serão re-colocados no tubo para continuar o seu turno.")

    @staticmethod
    def picked_dices(dices: list[str]) -> str:
        """Show picked dices.

        :param dices: List of dices.
        :return: String displaying picked dices.
        """
        text = "\nDados pegos do pote:"
        for dice_obj in dices:
            text += f"\n{INDENT}{dice_obj}"
        return text

    @staticmethod
    def rolled_dices(dices: list[str]) -> str:
        """Show rolled dices results.

        :param dices: List of dices.
        :return: String displaying rolled dices results.
        """
        text = "\nDados rolados:"
        for dice_obj in dices:
            text += f"\n{INDENT}{dice_obj}"
        return text

    @staticmethod
    def display_turn(name: str, stats: dict[str, int], dices: int, score: int) -> str:
        """Display the current turn status showing the player, amount of picked dices and player score.

        :param name: String of the player name.
        :param stats: Dict with the amount of dice sides accumulated during the turn.
        :param dices: Number of all dices picked byt the player.
        :param score: Player score.
        :return: String displaying current round info.
        """
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
    def enter_turn(round_count: int, name: int, score: int, current: int) -> str:
        """Announces the start of the player turn.

        :param round_count: Number of rounds already played.
        :param name: String of the player name.
        :param score: Number of accumulate points of the player through the game.
        :param current: Number of current turn points.
        :return: String announcing the start of the turn.
        """
        return (f"\n{'=' * TERMINAL_WIDTH}\n"
                f"{style(round_count, BOLD)}º Rodada, turno do(a) {style(name, BOLD, UND)}.\n"
                f"A sua pontuação atual é de {style(score, GREEN, BOLD, UND)}"
                f" pontos, o seu acumulado é {style(score + current, GREEN, BOLD, UND)} pontos;")

    @staticmethod
    def round_lost(name: str, shots: int) -> str:
        """Inform the player about the loss of the turn.

        :param name: String of the player name.
        :param shots: Number of shots player took during the turn.
        :return: String informing turn loss.
        """
        return f"\nO jogador {style(name, BOLD, UND)} acumulou "\
               f"{style(shots, RED, BOLD, UND)} tiros e perdeu o turno!"

    @staticmethod
    def ask_pick_dices(amount: int) -> str:
        """Prompt player to pick dices from the pool.

        :param amount: Number of dices to take.
        :return: String prompting the player to take the dices.
        """
        return f"\nPressione ENTER para pegar {style(amount, BOLD, UND)} dados do pote..."


class PlayerStrings:
    """Class to store all Player class related strings to be printed that interface with the user.
    """
    ask_name = "Nome do jogador: "

    @staticmethod
    def display_player(name: str, score: int) -> str:
        """Display player info.

        :param name: String of the player name.
        :param score: Number of accumulate points of the player through the game.
        :return: String of the player.
        """
        return f"{style(name, BOLD, UND)} fez {style(score, BOLD)} pontos."

    @staticmethod
    def ask_continue(dices: int) -> str:
        """Ask if player wants to continue playing the current turn.

        :param dices: Number of dices player needs to pick to continue playing.
        :return: String asking if the player wants to continue playing the current turn.
        """
        return f"\nPegar mais {style(dices, BOLD, UND)} dados e continuar jogando ou passar a vez? (s/n)"


class DiceStrings:
    """Class to store all Dice class related strings to be printed that interface with the user.
    """
    @staticmethod
    def display_dice(color: str, value: str) -> str:
        """Display dice.

        :param color: String of the dice color.
        :param value: String of the dice rolled side.
        :return: String displaying relevant info about the dice.
        """
        if not value:
            return f"Dado: {style(color.capitalize(), color)}"
        return f"Dado: {style(color.capitalize(), color):20}Lado: {style(value.capitalize(), BOLD)}"


class UtilsStrings:
    """Class to store all the utils functions strings that interface with the user.
    """
    str_warning = "Por favor entre uma resposta válida.\n"
    truthy = ("s",)
    falsy = ("n",)
    bool_warning = "Resposta invalida, por favor escreva sim ou não."

    @staticmethod
    def int_warning(min_val: int, max_val: int) -> str:
        """Display error message for integer out of the valid range.

        :param min_val: Number of the minimum value.
        :param max_val: Number of the maximum value.
        :return: String of the error message for integer out of the valid range.
        """
        return f"Por favor entre com um número inteiro entre {min_val} e {max_val}.\n"
