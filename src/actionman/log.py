from typing import Literal as _Literal
from pathlib import Path as _Path
from markitup import html as _html
from actionman import pprint as _pprint


class Logger:

    def __init__(
        self,
        realtime_output: bool = True,
        github_console: bool = True,
        output_html_filepath: str | _Path | None = "log.html",
        initial_section_level: _Literal[1, 2, 3, 4, 5] = 1,
        h1_kwargs: dict | None = None,
        h2_kwargs: dict | None = None,
        h3_kwargs: dict | None = None,
        h4_kwargs: dict | None = None,
        h5_kwargs: dict | None = None,
        h6_kwargs: dict | None = None,
        symbol_bulletpoint: str = "🔘",
        symbol_success: str = "✅",
        symbol_skip: str = "❎",
        symbol_error: str = "⛔",
        symbol_warning: str = "🚨",
        symbol_attention: str = "❗",
        entry_seperator_top: str = "="*35,
        entry_seperator_bottom: str = "="*35,
        entry_seperator_title: str = "-"*30,
    ):
        self.realtime_output = realtime_output
        self.github_console = github_console
        self.output_html_filepath = _Path(output_html_filepath).resolve() if output_html_filepath else None
        self.section_level = initial_section_level

        self._heading_kwargs = {
            1: h1_kwargs or {},
            2: h2_kwargs or {},
            3: h3_kwargs or {},
            4: h4_kwargs or {},
            5: h5_kwargs or {},
            6: h6_kwargs or {},
        }
        self._heading_pprint = {
            1: _pprint.h1,
            2: _pprint.h2,
            3: _pprint.h3,
            4: _pprint.h4,
            5: _pprint.h5,
            6: _pprint.h6,
        }
        self._bullet = symbol_bulletpoint
        self._status_symbol = {
            "success": symbol_success,
            "skip": symbol_skip,
            "error": symbol_error,
            "warning": symbol_warning,
            "attention": symbol_attention,
        }
        self._entry_seperator_top = entry_seperator_top
        self._entry_seperator_bottom = entry_seperator_bottom
        self._entry_seperator_title = entry_seperator_title

        if self.output_html_filepath:
            self.output_html_filepath.parent.mkdir(parents=True, exist_ok=True)
            self.output_html_filepath.touch(exist_ok=True)

        self._log_console: str = ""
        self._log_html: str = ""
        return

    @property
    def console_log(self):
        return self._log_console

    @property
    def html_log(self):
        return self._log_html

    def section(self, title: str):
        heading_html = _html.h(min(self.section_level + 1, 6), title)
        heading_console = self._heading_pprint[self.section_level](
            title, pprint=False, **self._heading_kwargs[self.section_level]
        )
        self._submit(console=heading_console, file=heading_html)
        self.section_level = min(self.section_level + 1, 6)
        return

    def entry(
        self,
        status: _Literal["info", "debug", "success", "error", "warning", "attention", "skip", "input"],
        title: str,
        summary: str = "",
        details: tuple[str, ...] | list[str] = tuple(),
    ):
        title_full = f"{self._status_symbol[status]} {title}"
        details_console = "\n".join([f"{self._bullet} {detail}" for detail in details])
        details_console_full = (
            f"{summary}\n{details_console}" if summary and details else f"{summary}{details_console}"
        )
        console_entry = _pprint.entry_github(
            title=title_full,
            details=details_console_full,
            pprint=False,
        ) if self.github_console else _pprint.entry_console(
            title=title_full,
            details=details_console_full,
            seperator_top=self._entry_seperator_top,
            seperator_bottom=self._entry_seperator_bottom,
            seperator_title=self._entry_seperator_title,
            pprint=False,
        )
        self._submit(console=console_entry, file="")
        return

    def section_end(self):
        self.section_level = max(self.section_level - 1, 1)
        return

    def _submit(self, console: str, file: str | _html.Element | _html.ElementCollection):
        console_entry = f"{console}\n"
        file_entry = f"{file}\n"
        self._log_console += console_entry
        self._log_html += file_entry
        if self.realtime_output:
            print(console)
            if self.output_html_filepath:
                with open(self.output_html_filepath, "a") as f:
                    f.write(file_entry)
        return


def logger(
    realtime_output: bool = True,
    github_console: bool = True,
    output_html_filepath: str | _Path | None = "log.html",
    initial_section_level: _Literal[1, 2, 3, 4, 5] = 1,
    h1_kwargs: dict | None = None,
    h2_kwargs: dict | None = None,
    h3_kwargs: dict | None = None,
    h4_kwargs: dict | None = None,
    h5_kwargs: dict | None = None,
    h6_kwargs: dict | None = None,
    symbol_bulletpoint: str = "🔘",
    symbol_success: str = "✅",
    symbol_skip: str = "❎",
    symbol_error: str = "⛔",
    symbol_warning: str = "🚨",
    symbol_attention: str = "❗",
    entry_seperator_top: str = "="*35,
    entry_seperator_bottom: str = "="*35,
    entry_seperator_title: str = "-"*30,
):
    return Logger(
        realtime_output=realtime_output,
        github_console=github_console,
        output_html_filepath=output_html_filepath,
        initial_section_level=initial_section_level,
        h1_kwargs=h1_kwargs,
        h2_kwargs=h2_kwargs,
        h3_kwargs=h3_kwargs,
        h4_kwargs=h4_kwargs,
        h5_kwargs=h5_kwargs,
        h6_kwargs=h6_kwargs,
        symbol_bulletpoint=symbol_bulletpoint,
        symbol_success=symbol_success,
        symbol_skip=symbol_skip,
        symbol_error=symbol_error,
        symbol_warning=symbol_warning,
        symbol_attention=symbol_attention,
        entry_seperator_top=entry_seperator_top,
        entry_seperator_bottom=entry_seperator_bottom,
        entry_seperator_title=entry_seperator_title,
    )