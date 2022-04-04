"""

Projeto:        Zombie Dice
Estudante:      André César Loezer
Curso:          Tecnologia em Análise em Desenvolvimento de Sistemas
Disciplina:     Raciocínio Computacional
Turma:          01

Obs:
    1 - If running on pycharm, in the "Edit Configurations" under "Execution"
        check the "Emulate terminal in output console" box
        If your terminal doesn't support ANSI colors, change variable USE_STYLES to False

    2 - Use python v3.10 or above, else the 2 "match" statements in the Player and Game classes will crash

"""


__author__ = "André César Loezer"
__version__ = "1.0.0"


from game import Game


if __name__ == '__main__':
    game = Game()
