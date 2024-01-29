from typing import Literal as _Literal
from markitup import sgr as _sgr


def github_group(title: str, details: str, pprint: bool = True) -> str:
    output = f"::group::{title}\n{details}\n::endgroup::"
    if pprint:
        print(output, flush=True)
    return output


def github_group_start(title: str, pprint: bool = True) -> str:
    output = f"::group::{title}"
    if pprint:
        print(output, flush=True)
    return output


def github_group_end(pprint: bool = True) -> str:
    output = "::endgroup::"
    if pprint:
        print(output, flush=True)
    return output


def github_log(
    message_type: _Literal["debug", "notice", "warning", "error"],
    message: str,
    title: str = "",
    filename: str = "",
    line_start: int = 0,
    line_end: int = 0,
    column_start: int = 0,
    column_end: int = 0,
    pprint: bool = True,
) -> str:
    """Create either a debug, notice, warning, or error log for GitHub Actions.

    Parameters
    ----------
    message_type : {"debug", "notice", "warning", "error"}
        The type of log to create.
    message : str
        The log message.
    title : str, optional
        The log title.
        This is not available (and will be ignored) for the "debug" log type.
    filename : str, optional
        Path to a file in the repository to associate the message with.
        This is not available (and will be ignored) for the "debug" log type.
    line_start : int, optional
        The starting line number in the file specified by the 'filename' argument,
        to associate the message with.
        This is not available (and will be ignored) for the "debug" log type.
    line_end : int, optional
        The ending line number in the file specified by the 'filename' argument,
        to associate the message with.
        This is not available (and will be ignored) for the "debug" log type.
    column_start : int, optional
        The starting column number in the line specified by the 'line_start' argument,
        to associate the message with.
        This is not available (and will be ignored) for the "debug" log type.
    column_end : int, optional
        The ending column number in the line specified by the 'line_start' argument,
        to associate the message with.
        This is not available (and will be ignored) for the "debug" log type.
    pprint : bool, default: True
        Whether to print the notice message to stdout.

    References
    ----------
    - [Debug](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-debug-message)
    - [Notice](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-notice-message)
    - [Warning](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-warning-message)
    - [Error](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-error-message)
    """
    args = locals()
    output = f"::{message_type} "
    args_added = False
    if message_type != "debug":
        for arg_name, github_arg_name in (
            ("title", "title"),
            ("filename", "file"),
            ("line_start", "line"),
            ("line_end", "endLine"),
            ("column_start", "col"),
            ("column_end", "endColumn"),
        ):
            if args[arg_name]:
                output += f"{github_arg_name}={args[arg_name]},"
                args_added = True
    else:
        message = f" {message}"
    output = output.removesuffix("," if args_added else " ")
    output += f"::{message}"
    if pprint:
        print(output, flush=True)
    return output


def entry_console(
    title: str,
    details: str = "",
    seperator_top: str = "="*35,
    seperator_bottom: str = "="*35,
    seperator_title: str = "-"*20,
    pprint: bool = True,
) -> str:
    output = ""
    if seperator_top:
        output += f"{seperator_top}\n"
    output += f"{title}"
    if seperator_title and details:
        output += f"\n{seperator_title}"
    if details:
        output += f"\n{details}"
    if seperator_bottom:
        output += f"\n{seperator_bottom}"
    if pprint:
        print(output, flush=True)
    return output


def h1(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (150, 0, 170),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h2(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (25, 100, 175),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h3(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (100, 160, 0),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h4(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (200, 150, 0),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h5(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (240, 100, 0),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h6(
    title: str,
    width: int = 0,
    align: _Literal["left", "right", "center"] = "left",
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (220, 0, 35),
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = True,
) -> str:
    return h(**locals())


def h(
    title: str,
    width: int,
    align: _Literal["left", "right", "center"],
    margin_top: int,
    margin_bottom: int,
    text_styles: str | int | list[str | int] | None = None,
    text_color: str | int | tuple[int, int, int] | None = None,
    background_color: str | int | tuple[int, int, int] | None = None,
    pprint: bool = False,
) -> str:
    control_sequence = _sgr.style(
        text_styles=text_styles, text_color=text_color, background_color=background_color
    )
    if align == "left":
        aligned_title = title.ljust(width)
    elif align == "right":
        aligned_title = title.rjust(width)
    else:
        aligned_title = title.center(width)
    heading_box = _sgr.format(text=aligned_title, control_sequence=control_sequence)
    margin_top = "\n" * margin_top
    margin_bottom = "\n" * margin_bottom
    output = f"{margin_top}{heading_box}{margin_bottom}"
    if pprint:
        print(output, flush=True)
    return output
