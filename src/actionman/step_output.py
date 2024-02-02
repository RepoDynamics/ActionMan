"""Work with the step output of the current step of a job run in a GitHub Actions workflow.

References
----------
- [GitHub Docs: Workflow Commands for GitHub Actions: Setting an output parameter](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter)
"""


import os as _os
from pathlib import Path as _Path

from actionman import _format
from actionman.exception import ActionManGitHubError as _ActionManGitHubError


def write(name: str, value: dict | list | tuple | str | bool | int | float | None) -> str:
    """Set a step's output parameter for the current step.

    This is done by writing the output
    to the environment file whose path is specified by the 'GITHUB_OUTPUT' environment variable.

    Parameters
    ----------
    name : str
        The name of the output parameter.
    value : dict | list | tuple | str | bool | int | float | None
        The value of the output parameter.
        If the value is not a string, it will be serialized and written as a JSON string.

    Returns
    -------
    str
        The output that was written to the file.
        This is only useful for logging/debugging purposes.

    Raises
    ------
    actionman.exception.ActionManOutputVariableTypeError
        If the value has an unsupported type.
    actionman.exception.ActionManOutputVariableSerializationError
        If the value could not be serialized to a JSON string.
    """
    output = _format.output_variable(name=name, value=value)
    with open(_FILEPATH, "a") as f:
        print(output, file=f)
    return output


def _get_filepath() -> _Path:
    env_var_name = "GITHUB_OUTPUT"
    path = _os.environ.get(env_var_name)
    if not path:
        raise _ActionManGitHubError(missing_env_var=env_var_name)
    return _Path(path)


_FILEPATH = _get_filepath()
