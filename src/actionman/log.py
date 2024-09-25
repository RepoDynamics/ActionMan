"""Create workflow annotations and logs for a GitHub Actions workflow run."""

from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from rich.console import Console, Group as _Group
from rich import segment as _segment
from rich.text import Text as _Text

if _TYPE_CHECKING:
    from typing import Literal
    from rich.console import RenderableType
    from rich.text import TextType
    from protocolman import Stringable


class Logger:

    def __init__(self, console: Console | dict | None = None):
        if not console:
            self.console = Console(
                color_system="truecolor",
                force_terminal=True,
                emoji_variant="emoji",
                width=90,
                safe_box=False,
            )
        elif isinstance(console, dict):
            self.console = Console(**console)
        else:
            self.console = console
        return


    def debug(self, *contents: RenderableType, out: bool = True) -> _Group:
        """Create a debug log.

        Parameters
        ----------
        contents : actionman.protocol.Stringable
            The log message.
        out : bool, default: True
            Whether to directly print the debug log.

        Returns
        -------
        str
            The debug log.

        References
        ----------
        - [GitHub Docs: Workflow Commands for GitHub Actions: Setting a debug message](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-debug-message)
        """
        final_lines: list[_segment.Segments] = []
        for content in contents:
            for line in self.console.render_lines(content):
                line.insert(0, _segment.Segment("::debug::"))
                final_lines.append(_segment.Segments(line))
        output = _Group(*final_lines)
        if out:
            self.console.print(output)
        return output


    def annotation(
        self,
        typ: Literal["notice", "warning", "error"],
        message: TextType,
        title: TextType = "",
        filename: Stringable = "",
        line_start: int = 0,
        line_end: int = 0,
        column_start: int = 0,
        column_end: int = 0,
        out: bool = True,
    ) -> _Text:
        """Create a notice, warning, or error annotation.

        Parameters
        ----------
        typ : {"notice", "warning", "error"}
            The type of annotation to create.
        message : actionman.protocol.Stringable
            The annotation message.
        title : actionman.protocol.Stringable, optional
            The annotation title.
        filename : actionman.protocol.Stringable, optional
            Path to a file in the repository to associate the message with.
        line_start : int, optional
            The starting line number in the file specified by the 'filename' argument,
            to associate the message with.
        line_end : int, optional
            The ending line number in the file specified by the 'filename' argument,
            to associate the message with.
        column_start : int, optional
            The starting column number in the line specified by the 'line_start' argument,
            to associate the message with.
        column_end : int, optional
            The ending column number in the line specified by the 'line_start' argument,
            to associate the message with.
        out : bool, default: True
            Whether to directly print the annotation.

        Returns
        -------
        str
            The annotation.

        References
        ----------
        - [GitHub Docs: Workflow Commands for GitHub Actions: Setting a notice message](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-notice-message)
        - [GitHub Docs: Workflow Commands for GitHub Actions: Setting a warning message](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-warning-message)
        - [GitHub Docs: Workflow Commands for GitHub Actions: Setting an error message](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-error-message)
        """
        args = locals()
        sig = []
        for arg_name, github_arg_name in (
            ("title", "title"),
            ("filename", "file"),
            ("line_start", "line"),
            ("line_end", "endLine"),
            ("column_start", "col"),
            ("column_end", "endColumn"),
        ):
            if args[arg_name]:
                sig.append(f"{github_arg_name}={args[arg_name]}")
        sig_str = ",".join(sig)
        sig_section = f" {sig_str}" if sig_str else ""
        output = _Text(f"::{typ}{sig_section}::")
        output.append(message)
        if out:
            self.console.print(output)
        return output


    def group(self, *contents: RenderableType, title: TextType | None = None, out: bool = True) -> _Group:
        """Create an expandable log group.

        Parameters
        ----------
        contents : actionman.protocol.Stringable
            The details of the log group.
        title : actionman.protocol.Stringable
            The title of the log group.
        out : bool, default: True
            Whether to directly print the log group.

        Returns
        -------
        str
            The log group.

        References
        ----------
        - [GitHub Docs: Workflow Commands for GitHub Actions: Grouping log output](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#grouping-log-output)
        """
        start = self.group_open(title, out=False)
        end = self.group_close(out=False)
        output = _Group(start, *contents, end)
        if out:
            self.console.print(output)
        return output


    def group_open(self, title: TextType | None = None, out: bool = True) -> _Text:
        """Open an expandable log group.

        Parameters
        ----------
        title : actionman.protocol.Stringable
            The title of the log group.
        out : bool, default: True
            Whether to directly print the log group.

        Returns
        -------
        str
            The log group's opening tag.

        References
        ----------
        - [GitHub Docs: Workflow Commands for GitHub Actions: Grouping log output](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#grouping-log-output)
        """
        output = _Text("::group::")
        if title:
            output.append(title)
        if out:
            self.console.print(output)
        return output


    def group_close(self, out: bool = True) -> str:
        """Close an expandable log group.

        Parameters
        ----------
        out
            Whether to directly print the log group.

        Returns
        -------
        The log group's closing tag.

        References
        ----------
        - [GitHub Docs: Workflow Commands for GitHub Actions: Grouping log output](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#grouping-log-output)
        """
        output = "::endgroup::"
        if out:
            self.console.print(output)
        return output
