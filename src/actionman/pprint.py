from markitup import sgr as _sgr


def entry_github(title: str, details: str, pprint: bool = True) -> str:
    output = f"::group::{title}\n{details}\n::endgroup::"
    if pprint:
        print(output)
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
        print(output)
    return output


def h1(
    title: str,
    width: int = 110,
    margin_top: int = 2,
    margin_bottom: int = 1,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (150, 0, 170),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h2(
    title: str,
    width: int = 95,
    margin_top: int = 1,
    margin_bottom: int = 1,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (25, 100, 175),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h3(
    title: str,
    width: int = 80,
    margin_top: int = 1,
    margin_bottom: int = 1,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (100, 160, 0),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h4(
    title: str,
    width: int = 65,
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (200, 150, 0),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h5(
    title: str,
    width: int = 50,
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (240, 100, 0),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h6(
    title: str,
    width: int = 35,
    margin_top: int = 1,
    margin_bottom: int = 0,
    text_styles: str | int | list[str | int] | None = "bold",
    text_color: str | int | tuple[int, int, int] | None = (255, 255, 255),
    background_color: str | int | tuple[int, int, int] | None = (220, 0, 35),
    pprint: bool = True,
) -> str:
    return h(**locals())


def h(
    title: str,
    width: int,
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
    centered_title = title.center(width)
    heading_box = _sgr.format(text=centered_title, control_sequence=control_sequence)
    margin_top = "\n" * margin_top
    margin_bottom = "\n" * margin_bottom
    output = f"{margin_top}{heading_box}{margin_bottom}"
    if pprint:
        print(output)
    return output
