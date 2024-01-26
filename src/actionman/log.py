from enum import Enum as _Enum
from typing import Literal as _Literal
import inspect as _inspect
import sys as _sys
import traceback as _traceback
from pathlib import Path as _Path
from markitup import html as _html, sgr as _sgr
from actionman import pprint as _pprint


class LogStatus(_Enum):
    PASS = "pass"
    SKIP = "skip"
    ATTENTION = "attention"
    WARN = "warn"
    FAIL = "fail"
    INFO = "info"


class Logger:

    def __init__(
        self,
        realtime_output: bool = True,
        github_console: bool = True,
        exit_code_on_error: int | None = 1,
        output_html_filepath: str | _Path | None = "log.html",
        initial_section_level: _Literal[1, 2, 3, 4, 5] = 1,
        h1_kwargs: dict | None = None,
        h2_kwargs: dict | None = None,
        h3_kwargs: dict | None = None,
        h4_kwargs: dict | None = None,
        h5_kwargs: dict | None = None,
        h6_kwargs: dict | None = None,
        symbol_bulletpoint: str = "🔘",
        symbol_caller: str = "🔔",
        symbol_pass: str = "✅",
        symbol_skip: str = "❎",
        symbol_attention: str = "❗",
        symbol_warn: str = "🚨",
        symbol_fail: str = "🚫",
        symbol_info: str = "ℹ️",
        symbol_input: str = "📥",
        symbol_output: str = "📤",
        symbol_debug: str = "🐞",
        symbol_error: str = "⛔",
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
        self._symbol_status = {
            LogStatus.PASS: symbol_pass,
            LogStatus.SKIP: symbol_skip,
            LogStatus.ATTENTION: symbol_attention,
            LogStatus.WARN: symbol_warn,
            LogStatus.FAIL: symbol_fail,
            LogStatus.INFO: symbol_info,
        }
        self._symbol = {
            "caller": symbol_caller,
            "bullet": symbol_bulletpoint,
            "error": symbol_error,
            "input": symbol_input,
            "output": symbol_output,
            "debug": symbol_debug,
        }
        self._entry_seperator_top = entry_seperator_top
        self._entry_seperator_bottom = entry_seperator_bottom
        self._entry_seperator_title = entry_seperator_title
        self._error_title = _pprint.h(
            title="ERROR",
            width=11,
            margin_top=0,
            margin_bottom=0,
            text_styles="bold",
            text_color=(0, 0, 0),
            background_color=(255, 0, 0),
        )

        error_msg_exit_code = (
            "Argument `exit_code_on_error` must be a positive integer or None, "
            f"but got '{exit_code_on_error}' (type: {type(exit_code_on_error)})."
        )
        if isinstance(exit_code_on_error, int):
            if exit_code_on_error <= 0:
                raise ValueError(error_msg_exit_code)
        elif exit_code_on_error is not None:
            raise TypeError(error_msg_exit_code)
        self._default_exit_code = exit_code_on_error

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

    def error(self, summary: str, details: str = "", sys_exit: bool | None = None, exit_code: int | None = None):
        caller = self._get_caller()
        symbol = self._symbol["error"] * 3
        summary_formatted = _sgr.format(
            summary,
            _sgr.style(text_styles="bold", text_color=(255, 0, 0))
        )
        error_msg = f"\n\n{symbol} {self._error_title} {symbol} {summary_formatted}\n{caller}"
        if details:
            details_formatted = _sgr.format(details, _sgr.style(text_styles="bold"))
            error_msg += f"\n{details_formatted}"
        traceback = _traceback.format_exc()
        if traceback != "NoneType: None\n":
            error_msg += f"\n\n{traceback}"
        print(error_msg, flush=True)
        if sys_exit is None:
            sys_exit = self._default_exit_code is not None
        if sys_exit:
            exit_code = exit_code or self._default_exit_code
            _sys.exit(exit_code)
        return

    def entry(
        self,
        status: LogStatus | _Literal["pass", "skip", "attention", "warn", "fail", "info"],
        title: str,
        summary: str = "",
        details: str | tuple[str, ...] | list[str] = tuple(),
    ):
        status = LogStatus(status) if isinstance(status, str) else status
        caller = self._get_caller()
        title_full = f"{self._symbol_status[status]} {title}"
        if isinstance(details, str):
            details = (details,)
        details_console = "\n".join([f"{self._bullet} {detail}" for detail in details] + [caller])
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
        html_details_content = []
        if summary:
            html_details_content.append(_html.p(summary))
        if details:
            html_details_content.append(_html.ul(details))
        details.append(caller)
        html_entry = _html.details(summary=title_full, content=html_details_content)
        self._submit(console=console_entry, file=html_entry)
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
            print(console, flush=True)
            if self.output_html_filepath:
                with open(self.output_html_filepath, "a") as f:
                    f.write(file_entry)
        return

    def _get_caller(self, stack_index: int = 3) -> str:
        stack = _inspect.stack()
        # The caller is the second element in the stack list
        caller_frame = stack[stack_index]
        module = _inspect.getmodule(caller_frame[0])
        module_name = module.__name__ if module else "<module>"
        # Get the function or method name
        func_name = caller_frame.function
        # Combine them to get a fully qualified name
        fully_qualified_name = f"{module_name}.{func_name}"
        caller_entry = f"{self._symbol['caller']} Caller: {fully_qualified_name}"
        return caller_entry


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
) -> Logger:
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
        symbol_pass=symbol_success,
        symbol_skip=symbol_skip,
        symbol_error=symbol_error,
        symbol_warn=symbol_warning,
        symbol_attention=symbol_attention,
        entry_seperator_top=entry_seperator_top,
        entry_seperator_bottom=entry_seperator_bottom,
        entry_seperator_title=entry_seperator_title,
    )