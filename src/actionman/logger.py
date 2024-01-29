from enum import Enum as _Enum
from typing import Literal as _Literal
import inspect as _inspect
import sys as _sys
import traceback as _traceback
from textwrap import dedent as _dedent
from pathlib import Path as _Path
from markitup import html as _html, sgr as _sgr
from actionman import pprint as _pprint


class LogLevel(_Enum):
    DEBUG = "debug"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Logger:

    def __init__(
        self,
        realtime_output: bool = True,
        github_console: bool = True,
        initial_section_number: int = 1,
        exit_code_critical: int | None = 1,
        console_print_debug: bool = True,
        output_html_filepath: str | _Path | None = "log.html",
        root_heading: str = "Log",
        html_title: str = "Log",
        html_style: str = "",
        h1_kwargs: dict | None = None,
        h2_kwargs: dict | None = None,
        h3_kwargs: dict | None = None,
        h4_kwargs: dict | None = None,
        h5_kwargs: dict | None = None,
        h6_kwargs: dict | None = None,
        debug_symbol: str = "🔘",
        debug_title_text_styles: str | int | list[str | int] | None = "bold",
        debug_title_text_color: str | int | tuple[int, int, int] | None = None,
        debug_title_background_color: str | int | tuple[int, int, int] | None = None,
        info_symbol: str = "ℹ️",
        info_title_text_styles: str | int | list[str | int] | None = "bold",
        info_title_text_color: str | int | tuple[int, int, int] | None = None,
        info_title_background_color: str | int | tuple[int, int, int] | None = None,
        notice_symbol: str = "❗",
        notice_title_text_styles: str | int | list[str | int] | None = "bold",
        notice_title_text_color: str | int | tuple[int, int, int] | None = None,
        notice_title_background_color: str | int | tuple[int, int, int] | None = None,
        warning_symbol: str = "🚨",
        warning_title_text_styles: str | int | list[str | int] | None = "bold",
        warning_title_text_color: str | int | tuple[int, int, int] | None = None,
        warning_title_background_color: str | int | tuple[int, int, int] | None = None,
        error_symbol: str = "🚫",
        error_title_text_styles: str | int | list[str | int] | None = "bold",
        error_title_text_color: str | int | tuple[int, int, int] | None = None,
        error_title_background_color: str | int | tuple[int, int, int] | None = None,
        critical_symbol: str = "⛔",
        critical_title_text_styles: str | int | list[str | int] | None = "bold",
        critical_title_text_color: str | int | tuple[int, int, int] | None = None,
        critical_title_background_color: str | int | tuple[int, int, int] | None = None,
        pass_symbol: str = "✅",
        caller_symbol: str = "🔔",
    ):
        self._realtime_output = realtime_output
        self._github_console = github_console
        self._output_html_filepath = _Path(output_html_filepath).resolve() if output_html_filepath else None
        self._print_debug = console_print_debug

        self._curr_section = ""
        self._next_section_num = [initial_section_number]
        self._open_grouped_sections = 0
        self._out_of_section: bool = False

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
        self._symbol_status = {
            LogLevel.DEBUG: debug_symbol,
            LogLevel.INFO: info_symbol,
            LogLevel.NOTICE: notice_symbol,
            LogLevel.WARNING: warning_symbol,
            LogLevel.ERROR: error_symbol,
            LogLevel.CRITICAL: critical_symbol,
        }
        self._symbol_pass = pass_symbol
        self._symbol_caller = caller_symbol

        self._style_status = {
            LogLevel.DEBUG: _sgr.style(
                text_styles=debug_title_text_styles,
                text_color=debug_title_text_color,
                background_color=debug_title_background_color,
            ),
            LogLevel.INFO: _sgr.style(
                text_styles=info_title_text_styles,
                text_color=info_title_text_color,
                background_color=info_title_background_color,
            ),
            LogLevel.NOTICE: _sgr.style(
                text_styles=notice_title_text_styles,
                text_color=notice_title_text_color,
                background_color=notice_title_background_color,
            ),
            LogLevel.WARNING: _sgr.style(
                text_styles=warning_title_text_styles,
                text_color=warning_title_text_color,
                background_color=warning_title_background_color,
            ),
            LogLevel.ERROR: _sgr.style(
                text_styles=error_title_text_styles,
                text_color=error_title_text_color,
                background_color=error_title_background_color,
            ),
            LogLevel.CRITICAL: _sgr.style(
                text_styles=critical_title_text_styles,
                text_color=critical_title_text_color,
                background_color=critical_title_background_color,
            ),
        }

        self._error_title = _pprint.h(
            title="ERROR",
            width=11,
            align="center",
            margin_top=0,
            margin_bottom=0,
            text_styles="bold",
            text_color=(0, 0, 0),
            background_color=(255, 0, 0),
        )

        error_msg_exit_code = (
            "Argument `exit_code_on_error` must be a positive integer or None, "
            f"but got '{exit_code_critical}' (type: {type(exit_code_critical)})."
        )
        if isinstance(exit_code_critical, int):
            if exit_code_critical <= 0:
                raise ValueError(error_msg_exit_code)
        elif exit_code_critical is not None:
            raise TypeError(error_msg_exit_code)
        self._default_exit_code = exit_code_critical

        if self._output_html_filepath:
            self._output_html_filepath.parent.mkdir(parents=True, exist_ok=True)
            self._output_html_filepath.touch(exist_ok=True)

        self._log_console: str = ""
        html_intro = _dedent(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>{html_title}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            """
        ).lstrip()
        if html_style:
            html_intro += f"<style>\n{html_style}\n</style>\n"
        self._log_html: str = f"{html_intro}</head>\n<body>\n"
        self._html_file_end = "</body>\n</html>\n"
        self._html_num_chars_at_end = -len(self._html_file_end)
        if self._realtime_output and self._output_html_filepath:
            with open(self._output_html_filepath, 'w') as f:
                f.write(f"{self._log_html}{self._html_file_end}")
        self.section(title=root_heading, stack_up=1)
        return

    def section(self, title: str, group: bool = False, stack_up: int = 0):
        section_level = min(len(self._next_section_num), 6)
        section_num = ".".join([str(num) for num in self._next_section_num])
        self._curr_section = f"{section_num}  {title}"
        fully_qualified_name = self._caller_name(stack_up=stack_up)
        caller_entry_html = f"{self._symbol_caller} Caller: <code>{fully_qualified_name}</code>"
        heading_html = _html.h(section_level, self._curr_section)
        output_html = f"{heading_html}\n{caller_entry_html}"
        heading_console = self._heading_pprint[section_level](
            self._curr_section, pprint=False, **self._heading_kwargs[section_level]
        )
        output_console = f"{heading_console}  [{fully_qualified_name}]"
        if self._github_console:
            if group and not self._open_grouped_sections:
                output_console = _pprint.github_group_start(title=output_console, pprint=False)
            if group or self._open_grouped_sections:
                self._open_grouped_sections += 1
        self._submit(console=output_console, file=output_html)
        self._next_section_num.append(1)
        return

    def section_end(self):
        if self._open_grouped_sections:
            self._open_grouped_sections -= 1
            if not self._open_grouped_sections:
                self._submit_console(text=_pprint.github_group_end(pprint=False))
        if len(self._next_section_num) > 2:
            self._next_section_num.pop()
        else:
            # TODO: Give some warning or raise some error here
            pass
        self._next_section_num[-1] += 1
        self._out_of_section = True
        return

    def log(
        self,
        level: LogLevel | _Literal["debug", "info", "notice", "warning", "error", "critical"],
        message: str,
        title: str = "",
        code: str = "",
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        stack_up: int = 0,
    ):
        level = level if isinstance(level, LogLevel) else LogLevel(level)
        kwargs = {"message": message, "title": title, "code": code}
        if level is LogLevel.CRITICAL:
            kwargs |= {"sys_exit": sys_exit, "exit_code": exit_code, "stack_up": stack_up + 1}
        getattr(self, level.value)(**kwargs)
        return

    def debug(self, message: str, title: str = "", code: str = "") -> None:
        output_console, output_html, _ = self._format_entry(
            level=LogLevel.DEBUG,
            message=message,
            title=title,
            code=code,
        )
        if self._github_console:
            output_console = _pprint.github_log(
                message_type="debug",
                message=output_console,
                pprint=False,
            )
        self._submit(console=output_console, file=output_html, is_debug=True)
        return

    def info(self, message: str, title: str = "", code: str = "") -> None:
        output_console, output_html, _ = self._format_entry(
            level=LogLevel.INFO,
            message=message,
            title=title,
            code=code,
        )
        self._submit(console=output_console, file=output_html)
        return

    def notice(self, message: str, title: str = "", code: str = "") -> None:
        output_console, output_html, github_annotation_msg = self._format_entry(
            level=LogLevel.NOTICE,
            message=message,
            title=title,
            code=code,
        )
        self._submit(console=output_console, file=output_html)
        if self._github_console:
            _pprint.github_log(
                message_type="notice",
                message=github_annotation_msg,
                title=self._curr_section,
            )
        return

    def warning(self, message: str, title: str = "", code: str = "") -> None:
        output_console, output_html, github_annotation_msg = self._format_entry(
            level=LogLevel.WARNING,
            message=message,
            title=title,
            code=code,
        )
        self._submit(console=output_console, file=output_html)
        if self._github_console:
            _pprint.github_log(
                message_type="warning",
                message=github_annotation_msg,
                title=self._curr_section,
            )
        return

    def error(self, message: str, title: str = "", code: str = "") -> None:
        output_console, output_html, github_annotation_msg = self._format_entry(
            level=LogLevel.ERROR,
            message=message,
            title=title,
            code=code,
        )
        self._submit(console=output_console, file=output_html)
        if self._github_console:
            _pprint.github_log(
                message_type="error",
                message=github_annotation_msg,
                title=self._curr_section,
            )
        return

    def critical(
        self,
        message: str,
        title: str = "",
        code: str = "",
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        stack_up: int = 0,
    ):
        traceback = _traceback.format_exc()
        if traceback != "NoneType: None\n":
            code += f"\n\n{traceback}"
            code = code.strip()
        output_console, output_html, github_annotation_msg = self._format_entry(
            level=LogLevel.CRITICAL,
            message=message,
            title=title,
            code=code,
        )
        _sys.stdout.flush()  # Flush stdout buffer before printing the exception
        _sys.stderr.flush()  # Flush stderr buffer before printing the exception
        self._submit(console=output_console, file=output_html)
        if sys_exit is None:
            sys_exit = self._default_exit_code is not None
        if sys_exit and self._open_grouped_sections:
            self._submit_console(text=_pprint.github_group_end(pprint=False))
        if self._github_console:
            caller_name = self._caller_name(stack_up=stack_up)
            _pprint.github_log(
                message_type="error",
                message=github_annotation_msg,
                title=f"FATAL ERROR: {self._curr_section} (caller: {caller_name})",
            )
        if sys_exit:
            exit_code = exit_code or self._default_exit_code
            _sys.exit(exit_code)
        return

    # def entry(
    #     self,
    #     status: LogLevel | _Literal["pass", "skip", "attention", "warn", "fail", "info"],
    #     title: str,
    #     summary: str = "",
    #     details: str | tuple[str, ...] | list[str] = tuple(),
    # ):
    #     status = LogLevel(status) if isinstance(status, str) else status
    #     caller = self._caller_name()
    #     title_full = f"{self._symbol_status[status]} {title}"
    #     if isinstance(details, str):
    #         details = (details,)
    #     details_console = "\n".join([f"{self._bullet} {detail}" for detail in details] + [caller])
    #     details_console_full = (
    #         f"{summary}\n{details_console}" if summary and details else f"{summary}{details_console}"
    #     )
    #     console_entry = _pprint.github_group(
    #         title=title_full,
    #         details=details_console_full,
    #         pprint=False,
    #     ) if self._github_console else _pprint.entry_console(
    #         title=title_full,
    #         details=details_console_full,
    #         seperator_top=self._entry_seperator_top,
    #         seperator_bottom=self._entry_seperator_bottom,
    #         seperator_title=self._entry_seperator_title,
    #         pprint=False,
    #     )
    #     html_details_content = []
    #     if summary:
    #         html_details_content.append(_html.p(summary))
    #     if details:
    #         html_details_content.append(_html.ul(details))
    #     details.append(caller)
    #     html_entry = _html.details(summary=title_full, content=html_details_content)
    #     self._submit(console=console_entry, file=html_entry)
    #     return

    @property
    def console_log(self):
        return self._log_console

    @property
    def html_log(self):
        return f"{self._log_html}{self._html_file_end}"

    def _submit(
        self,
        console: str,
        file: str | _html.Element | _html.ElementCollection,
        is_debug: bool = False
    ):
        self._submit_console(text=console, is_debug=is_debug)
        self._submit_html(html=file)
        return

    def _submit_console(self, text: str, is_debug: bool = False):
        self._log_console += f"{text}\n"
        if self._realtime_output and (not is_debug or self._github_console or self._print_debug):
            print(text, flush=True)
        return

    def _submit_html(self, html: str | _html.Element | _html.ElementCollection):
        file_entry = f"{html}\n"
        self._log_html += file_entry
        if self._realtime_output and self._output_html_filepath:
            with open(self._output_html_filepath, 'rb+') as file:
                file.seek(self._html_num_chars_at_end, 2)
                file.write(f"{file_entry}{self._html_file_end}".encode('utf-8'))
        return

    def _format_entry(self, level: LogLevel, message: str, title: str = "", code: str = ""):
        symbol = self._symbol_status[level]
        if title:
            title_console_formatted = _sgr.format(text=title, control_sequence=self._style_status[level])
            title_console = f"{title_console_formatted}: "
            title_html = f"<b>{title}</b>: "
            title_annotation = f"{title}: "
        else:
            title_console = ""
            title_html = ""
            title_annotation = ""
        if code:
            code_console = f"\n{code}"
            code_html = f"<pre>{code}</pre>"
        else:
            code_console = ""
            code_html = ""
        output_console = f"{symbol} {title_console}{message}{code_console}"
        output_html = _html.ul([f"{symbol} {title_html}{message}{code_html}"])
        github_annotation_msg = f"{title_annotation}{message}"
        return output_console, output_html, github_annotation_msg

    @staticmethod
    def _caller_name(stack_up: int = 0) -> str:
        stack = _inspect.stack()
        # The caller is the second element in the stack list
        caller_frame = stack[2 + stack_up]
        module = _inspect.getmodule(caller_frame[0])
        module_name = module.__name__ if module else "<module>"
        # Get the function or method name
        func_name = caller_frame.function
        # Combine them to get a fully qualified name
        fully_qualified_name = f"{module_name}.{func_name}"
        return fully_qualified_name


def create(
    realtime_output: bool = True,
    github_console: bool = True,
    initial_section_number: int = 1,
    exit_code_critical: int | None = 1,
    console_print_debug: bool = True,
    output_html_filepath: str | _Path | None = "log.html",
    root_heading: str = "Log",
    html_title: str = "Log",
    html_style: str = "",
    h1_kwargs: dict | None = None,
    h2_kwargs: dict | None = None,
    h3_kwargs: dict | None = None,
    h4_kwargs: dict | None = None,
    h5_kwargs: dict | None = None,
    h6_kwargs: dict | None = None,
    debug_symbol: str = "🔘",
    debug_title_text_styles: str | int | list[str | int] | None = "bold",
    debug_title_text_color: str | int | tuple[int, int, int] | None = None,
    debug_title_background_color: str | int | tuple[int, int, int] | None = None,
    info_symbol: str = "ℹ️",
    info_title_text_styles: str | int | list[str | int] | None = "bold",
    info_title_text_color: str | int | tuple[int, int, int] | None = None,
    info_title_background_color: str | int | tuple[int, int, int] | None = None,
    notice_symbol: str = "❗",
    notice_title_text_styles: str | int | list[str | int] | None = "bold",
    notice_title_text_color: str | int | tuple[int, int, int] | None = None,
    notice_title_background_color: str | int | tuple[int, int, int] | None = None,
    warning_symbol: str = "🚨",
    warning_title_text_styles: str | int | list[str | int] | None = "bold",
    warning_title_text_color: str | int | tuple[int, int, int] | None = None,
    warning_title_background_color: str | int | tuple[int, int, int] | None = None,
    error_symbol: str = "🚫",
    error_title_text_styles: str | int | list[str | int] | None = "bold",
    error_title_text_color: str | int | tuple[int, int, int] | None = None,
    error_title_background_color: str | int | tuple[int, int, int] | None = None,
    critical_symbol: str = "⛔",
    critical_title_text_styles: str | int | list[str | int] | None = "bold",
    critical_title_text_color: str | int | tuple[int, int, int] | None = None,
    critical_title_background_color: str | int | tuple[int, int, int] | None = None,
    pass_symbol: str = "✅",
    caller_symbol: str = "🔔",
) -> Logger:
    return Logger(**locals())
