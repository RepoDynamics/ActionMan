from types import NoneType as _NoneType
import base64 as _base64
import json as _json

from actionman.exception import (
    ActionManOutputVariableTypeError as _ActionManOutputVariableTypeError,
    ActionManOutputVariableSerializationError as _ActionManOutputVariableSerializationError,
)


def output_variable(name: str, value: dict | list | tuple | str | bool | int | float | None) -> str:
    """Format a variable name and value to a string
    that could be written as an environment variable (to 'GITHUB_ENV')
    or output parameter (to 'GITHUB_OUTPUT') in a job step of a GitHub Actions workflow.

    Parameters
    ----------
    name : str
        The name of the variable.
    value : dict | list | tuple | str | bool | int | float | None
        The value of the variable.

    Returns
    -------
    str
        The formatted variable name and value
        as a string ready to be added to 'GITHUB_ENV' or 'GITHUB_OUTPUT'.

    Raises
    ------
    Actionman.exception.ActionManOutputVariableTypeError
        If the value has an unsupported type.
    Actionman.exception.ActionManOutputVariableSerializationError
        If the value could not be serialized to a JSON string.

    References
    ----------
    - [GitHub Docs: Workflow commands for GitHub Actions: Setting an environment variable](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable)
    - [GitHub Docs: Workflow commands for GitHub Actions: Setting an output parameter](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter)
    """
    if isinstance(value, str):
        if "\n" in value:
            with open("/dev/urandom", "rb") as f:
                random_bytes = f.read(15)
            random_delimeter = _base64.b64encode(random_bytes).decode("utf-8")
            return f"{name}<<{random_delimeter}\n{value}\n{random_delimeter}"
    elif isinstance(value, (dict, list, tuple, bool, int, float, _NoneType)):
        try:
            value = _json.dumps(value)
        except Exception as e:
            raise _ActionManOutputVariableSerializationError(
                var_name=name,
                var_value=value,
                exception=e,
            ) from e
    else:
        raise _ActionManOutputVariableTypeError(
            var_name=name,
            var_value=value,
        )
    return f"{name}={value}"
