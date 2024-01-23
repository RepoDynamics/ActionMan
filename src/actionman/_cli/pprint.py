import argparse
from pathlib import Path
from actionman import pprint


def h1():
    kwargs = get_args_heading()
    pprint.h1(**kwargs)
    return


def h2():
    kwargs = get_args_heading()
    pprint.h2(**kwargs)
    return


def h3():
    kwargs = get_args_heading()
    pprint.h3(**kwargs)
    return


def h4():
    kwargs = get_args_heading()
    pprint.h4(**kwargs)
    return


def h5():
    kwargs = get_args_heading()
    pprint.h5(**kwargs)
    return


def h6():
    kwargs = get_args_heading()
    pprint.h6(**kwargs)
    return


def entry_github() -> None:
    kwargs = get_args_entry_gh()
    pprint.entry_github(**kwargs)
    return


def file():
    args = get_args_file()
    content = Path(args.path).read_text()
    if args.strip:
        content = content.strip()
    margin_top = "\n" * args.margin
    margin_bottom = margin_top if content.endswith("\n") else f"{margin_top}\n"
    print(f"{margin_top}{content}{margin_bottom}", flush=True)
    return


def get_args_heading() -> dict:

    def parse_text_styles(styles: list | None):
        if styles is None:
            return
        if len(styles) == 1 and styles[0].lower() == "false":
            return False
        return [int(style) if style.isdigit() else style for style in kwargs.text_styles]

    def parse_color(color: list | None):
        if color is None:
            return
        if len(color) == 1:
            color = color[0]
            if color.lower() == "false":
                return False
            return int(color) if color.isdigit() else color
        if len(color) != 3:
            raise ValueError(f"Invalid text color: {color}")
        parsed_color = []
        for c in color:
            if c.isdigit():
                parsed_color.append(int(c))
            else:
                raise ValueError(f"Invalid text color: {color}")
        return tuple(parsed_color)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "title",
        type=str, help="Heading title."
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=None,
        help="Width of the heading box in characters."
    )
    parser.add_argument(
        "-mt", "--margin-top",
        type=int,
        default=None,
        help="Number of blank lines to print before the heading box."
    )
    parser.add_argument(
        "-mb", "--margin-bottom",
        type=int,
        default=None,
        help="Number of blank lines to print after the heading box."
    )
    parser.add_argument(
        "-ts", "--text-styles",
        type=str,
        default=None,
        nargs="+",
        help=(
            "One or more text styles to apply to the heading title, "
            "each denoted either as an integer or string from the following list: "
            "0: normal, 1: bold, 2: faint, 3: italic, 4: underline, "
            "5: blink, 6: blink_fast, 7: reverse, 8: conceal, 9: strike. "
            "Set to 'false' to disable all text styles."
        )
    )
    parser.add_argument(
        "-tc", "--text-color",
        type=str,
        default=None,
        nargs="+",
        help=(
            "Text color of the heading title, "
            "denoted either as three integers representing the RGB value, "
            "or as an integer or string from the following list: "
            "30: black, 31: red, 32: green, 33: yellow, 34: blue, 35: magenta, 36: cyan, 37: white, "
            "90: b_black, 91: b_red, 92: b_green, 93: b_yellow, "
            "94: b_blue, 95: b_magenta, 96: b_cyan, 97: b_white. "
            "Set to 'false' to disable text color."
        )
    )
    parser.add_argument(
        "-bc", "--background-color",
        type=str,
        default=None,
        nargs="+",
        help=(
            "Background color of the heading title, "
            "denoted either as three integers representing the RGB value, "
            "or as an integer or string from the following list: "
            "40: black, 41: red, 42: green, 43: yellow, 44: blue, 45: magenta, 46: cyan, 47: white, "
            "100: b_black, 101: b_red, 102: b_green, 103: b_yellow, "
            "104: b_blue, 105: b_magenta, 106: b_cyan, 107: b_white. "
            "Set to 'false' to disable background color."
        )
    )

    kwargs = parser.parse_args()
    kwargs.text_styles = parse_text_styles(kwargs.text_styles)
    kwargs.text_color = parse_color(kwargs.text_color)
    kwargs.background_color = parse_color(kwargs.background_color)
    return {param: arg for param, arg in vars(kwargs).items() if arg is not None}


def get_args_entry_gh() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", type=str, help="Summary of the data.")
    parser.add_argument("details", type=str, help="Details of the data.")
    args = parser.parse_args()
    return vars(args)


def get_args_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to the file.")
    parser.add_argument(
        "-m", "--margin",
        type=int,
        required=False,
        default=2,
        help="Number of blank lines to add to the top and bottom of the file."
    )
    parser.add_argument(
        "-s", "--strip",
        action="store_true",
        help="Strip the file of leading and trailing whitespace before applying the margin."
    )
    return parser.parse_args()

