"""Style strings in the terminal output.
"""


from config import RED, YELLOW, GREEN, USE_STYLES


# Style identifiers
BOLD = "bold"
UND = "underline"


# Style options
STYLE = {
    RED: "\033[91m",
    YELLOW: "\033[93m",
    GREEN: "\033[92m",
    BOLD: "\033[1m",
    UND: "\033[4m",
}


def style_text(text: str or int, *styles: str) -> str:
    """Apply styles to text.

    :param text: Text to style.
    :param styles: List of styles.
    :return: Styled text.
    """
    # In case ANSI styles aren't compatible with the terminal
    if not USE_STYLES:
        return text
    output = ""

    # Add all styles
    for style in styles:
        output += STYLE[style]

    # Add text and reset style
    closing_style = "\033[0m"
    output += f"{text}{closing_style}"
    return output
