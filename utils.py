"""Miscellaneous functions goes in here.
"""


from os import system
from config import OS
from strings import UtilsStrings as Strings


def clear_console() -> None:
    """Clear console terminal.
    """
    command = "clear"
    if OS in ("nt", "dos"):
        command = "cls"
    system(command)


def char_input() -> str:
    """Capture and return a single character representing the key pressed.

    :return: Character pressed.
    """
    if OS in ("nt", "dos"):  # Get key on Windows
        import msvcrt
        key = msvcrt.getwche()
    else:  # Get key on UNIX
        # Solution found on:
        # https://www.semicolonworld.com/question/42804/python-read-a-single-character-from-the-user#comment-21
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


def int_input(message: str, min_val: int, max_val: int) -> int:
    """Get and validate integer input.

    :param message: Message prompting the user to enter an integer.
    :param min_val: Minimum valid value for the integer.
    :param max_val: Maximum valid value for the integer.
    :return: Validated integer input.
    """
    while True:
        response = input(message)
        try:
            # Input cannot be empty
            if not response:
                raise ValueError
            response = int(response)
            # Input must be between given interval
            if response > max_val or response < min_val:
                raise ValueError
        except ValueError:
            print(Strings.int_warning(min_val, max_val))
        else:
            return response


def text_input(message: str) -> str:
    """Get and validate string input.

    :param message: Message prompting the user to enter a string.
    :return: Validated string input.
    """
    while True:
        response = input(message)
        if response:
            return response
        print(Strings.str_warning)


def bool_input(message: str) -> bool:
    """Get and validate a boolean input.

    :param message: Message prompting the user to choose between true or false.
    :return: Boolean choice from the user.
    """
    while True:
        print(message)
        response = char_input().lower()
        print()
        if response in Strings.truthy:
            return True
        elif response in Strings.falsy:
            return False
        else:
            print(Strings.bool_warning)
