import subprocess as _subprocess
from pathlib import Path as _Path
from typing import NamedTuple as _NamedTuple


class ShellOutput(_NamedTuple):
    cmd: str
    out: str | bytes | None = None
    err: str | bytes | None = None
    code: int | None = None

    @property
    def executed(self) -> bool:
        return self.code is not None

    @property
    def success(self) -> bool:
        return self.code == 0

    @property
    def details(self) -> tuple[str, ...]:
        details = (
            f"Command: {self.cmd}",
            f"Executed: {self.executed}",
            f"Exit Code: {self.code}",
            f"Output: {self.out or None}",
            f"Error: {self.err or None}",
        )
        return details

    @property
    def summary(self) -> str:
        if not self.executed:
            return f"Command could not be executed."
        if not self.success:
            return f"Command failed with exit code {self.code}."
        return f"Command executed successfully."


def run(
    command: list[str],
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput:
    cmd_str = " ".join(command)
    try:
        process = _subprocess.run(command, text=text_output, cwd=cwd, capture_output=True)
    except FileNotFoundError:
        return ShellOutput(cmd=cmd_str)
    out = process.stdout.strip() if text_output else process.stdout
    err = process.stderr.strip() if text_output else process.stderr
    code = process.returncode
    return ShellOutput(cmd=cmd_str, out=out or None, err=err or None, code=code)


def python(
    command: list[str],
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return run(command=["python", *command], cwd=cwd, text_output=text_output)


def python_module(
    command: list[str],
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return python(command=["-m", *command], cwd=cwd, text_output=text_output)


def pip(
    command: list[str],
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return python_module(command=["pip", *command], cwd=cwd, text_output=text_output)


def pip_list(
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return pip(command=["list"], cwd=cwd, text_output=text_output)


def pip_install(
    command: list[str],
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return pip(command=["install", *command], cwd=cwd, text_output=text_output)


def pip_install_requirements(
    path: str | _Path,
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    return pip_install(command=["-r", str(path)], cwd=cwd, text_output=text_output)


def pip_install_package(
    name: str,
    requirement_specifier: str | None = None,
    upgrade: bool = False,
    install_dependencies: bool = True,
    index: str | None = None,
    cwd: str | _Path | None = None,
    text_output: bool = True,
) -> ShellOutput | None:
    index_name_url = {
        "testpypi": "https://test.pypi.org/simple/",
    }
    command = []
    if upgrade:
        command.append("--upgrade")
    command.append(f"{name}{requirement_specifier or ''}")
    if not install_dependencies:
        command.append("--no-deps")
    if index:
        index_url = index_name_url.get(index) or index
        command.extend(["--index-url", index_url])
    return pip_install(command=command, cwd=cwd, text_output=text_output)
