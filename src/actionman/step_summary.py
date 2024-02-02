"""Work with the step summary of the current step of a job run in a GitHub Actions workflow.

References
----------
- [GitHub Docs: Workflow Commands for GitHub Actions: Adding a job summary](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary)
"""


import os as _os
from pathlib import Path as _Path

from actionman.protocol import Stringable as _Stringable
from actionman.exception import ActionManGitHubError as _ActionManGitHubError


def filepath() -> _Path:
    """Return the path to the file where the step summary is stored."""
    return _FILEPATH


def read() -> str | None:
    """Read the current step summary contents from the file."""
    return _FILEPATH.read_text() if _FILEPATH.is_file() else None


def append(content: _Stringable) -> None:
    """Append the given content to the step summary file."""
    with open(_FILEPATH, "a") as f:
        print(content, file=f)
    return


def write(content: _Stringable) -> None:
    """Overwrite the step summary file with the given content."""
    with open(_FILEPATH, "w") as f:
        print(content, file=f)
    return


def remove() -> None:
    """Remove all step summary contents by deleting the file."""
    _FILEPATH.unlink()
    return


def _get_filepath() -> _Path:
    env_var_name = "GITHUB_STEP_SUMMARY"
    path = _os.environ.get(env_var_name)
    if not path:
        raise _ActionManGitHubError(missing_env_var=env_var_name)
    return _Path(path)


_FILEPATH = _get_filepath()
