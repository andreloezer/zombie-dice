"""

    All the logic to style strings in the terminal output

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


# Style text with given styles
def style_text(text, *styles):
    # In case style is not compatible with current terminal
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
