"""

    All miscellaneous functions goes in here

"""


from os import system
from config import OS
from strings import UtilsStrings as Strings


# Clear console
def clear_console():
    command = "clear"
    if OS in ["nt", "dos"]:
        command = "cls"
    system(command)


# Capture single key stroke
def char_input():
    if OS in ["nt", "dos"]:  # Get key on Windows
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


# Get and validate integer input
def int_input(message, min_val, max_val):
    while True:
        response = input(message)
        try:
            # Check if input is empty
            if not response:
                raise ValueError
            response = int(response)
            # Check if input is between given interval
            if response > max_val or response < min_val:
                raise ValueError
        except ValueError:
            print(Strings.int_warning(min_val, max_val))
        else:
            return response


# Get text input
def text_input(message):
    while True:
        response = input(message)
        if response:
            return response
        print(Strings.str_warning)


# Get boolean input
def bool_input(message):
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
