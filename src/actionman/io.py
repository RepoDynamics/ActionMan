from typing import Callable as _Callable, get_type_hints as _get_type_hints, Type as _Type
import os as _os
import json as _json
import inspect as _inspect
import base64 as _base64

from actionman.logger import Logger as _Logger, LogLevel as _LogLevel


def read_environment_variable(
    name: str,
    typ: _Type[str | bool | int | float | list | dict] = str,
    required: bool = True,
    mask_value: bool = False,
    logger: _Logger | None = None,
) -> str | bool | int | float | list | dict | None:
    """
    Parse inputs from environment variables.
    """
    def log(
        level: _LogLevel,
        message: str,
        title: str = "",
        code: str = "",
        exception_type: _Type[Exception] = ValueError,
        exception: Exception | None = None,
    ):
        if logger:
            logger.log(level=level, message=message, title=title, code=code)
            logger.section_end()
        if level is _LogLevel.CRITICAL:
            if exception:
                raise exception_type(message) from exception
            else:
                raise exception_type(message)
        return

    def raise_casting_error(expected_typ: str, exception: Exception | None = None):
        log(
            level=_LogLevel.CRITICAL,
            message=f"Environment variable {name} could not be cast to {expected_typ}.",
            title="Type Error",
            code=f"Value: {'**REDACTED**' if mask_value else value}",
            exception_type=TypeError,
            exception=exception,
        )
        return

    if logger:
        logger.section(title=f"Read Environment Variable '{name}'", group=True)
        logger.debug(f"Type: {typ.__name__}, Required: {required}, Mask Value: {mask_value}")
    value = _os.environ.get(name)
    if value is None:
        if required:
            log(level=_LogLevel.CRITICAL, message=f"Required environment variable '{name}' is not set.")
        log(
            level=_LogLevel.INFO,
            message=f"Optional environment variable '{name}' is not set."
        )
        return
    if typ is str:
        if isinstance(value, str):
            value_casted = value
        else:
            try:
                value_casted = str(value)
            except Exception as e:
                raise_casting_error(expected_typ="string", exception=e)
    elif typ is bool:
        if isinstance(value, bool):
            value_casted = value
        elif isinstance(value, str) and value.lower() in ("true", "false", ""):
            value_casted = value.lower() == "true"
        else:
            raise_casting_error(expected_typ="boolean")
    elif typ is int:
        if isinstance(value, int):
            value_casted = value
        elif isinstance(value, str):
            try:
                value_casted = int(value)
            except Exception as e:
                raise_casting_error(expected_typ="integer", exception=e)
        else:
            raise_casting_error(expected_typ="integer")
    elif typ is float:
        if isinstance(value, float):
            value_casted = value
        elif isinstance(value, str):
            try:
                value_casted = float(value)
            except Exception as e:
                raise_casting_error(expected_typ="float", exception=e)
        else:
            raise_casting_error(expected_typ="float")
    elif typ is list:
        if isinstance(value, list):
            value_casted = value
        elif isinstance(value, str):
            try:
                value_casted = _json.loads(value, strict=False)
            except Exception as e:
                raise_casting_error(expected_typ="list", exception=e)
        else:
            raise_casting_error(expected_typ="list")
    elif typ is dict:
        if isinstance(value, dict):
            value_casted = value
        elif isinstance(value, str):
            try:
                value_casted = _json.loads(value, strict=False)
            except Exception as e:
                raise_casting_error(expected_typ="dict", exception=e)
        else:
            raise_casting_error(expected_typ="dict")
    else:
        raise TypeError(f"The specified type '{typ}' for environment variable '{name}' is not supported.")
    if logger:
        logger.info(message=f"Successfully read and cast environment variable '{name}' to '{typ}'.")
        logger.debug(message="Value:", code='**REDACTED**' if mask_value else value)
        logger.section_end()
    return value_casted


def read_environment_variables(
    *variables_data: tuple[str, _Type[str | bool | int | float | list | dict], bool, bool],
    name_prefix: str = "",
    logger: _Logger | None = None,
    log_section_name: str = "Read Environment Variables",
) -> dict[str, str | bool | int | float | list | dict | None]:
    """
    Parse inputs from environment variables.
    """
    if logger:
        logger.section(log_section_name, group=True)
    variables = {}
    for name, typ, required, mask_value in variables_data:
        variables[name] = read_environment_variable(
            name=f"{name_prefix}{name}",
            typ=typ,
            required=required,
            logger=logger,
            mask_value=mask_value,
        )
    if logger:
        logger.section_end()
    return variables


def read_function_args_from_environment_variables(
    function: _Callable,
    name_prefix: str = "",
    mask_args: tuple[str, ...] | list[str] = tuple(),
    ignore_params: tuple[str, ...] | list[str] = tuple(),
    logger: _Logger | None = None,
    log_section_name: str = "Read Function Inputs From Environment Variables",
) -> dict[str, str | bool | int | float | list | dict | None]:
    """
    Parse inputs from environment variables.
    """
    if logger:
        logger.section(log_section_name.format(function=function.__qualname__), group=True)
        logger.debug(message="Function:", code=function.__qualname__)
        logger.debug(message="Name Prefix:", code=name_prefix)
        logger.debug(message="Masked Arguments:", code=str(mask_args))
        logger.debug(message="Ignored Parameters:", code=str(ignore_params))
    default_args = {
        k: v.default for k, v in _inspect.signature(function).parameters.items()
        if v.default is not _inspect.Parameter.empty
    }
    params = _get_type_hints(function)
    params.pop("return", None)
    if logger:
        logger.debug(message="Default Arguments:", code=str(default_args))
        logger.debug(message="Parameters:", code=str(params))
    args = {}
    for name, typ in params.items():
        if name not in ignore_params:
            arg = read_environment_variable(
                name=f"{name_prefix}{name}".upper(),
                typ=typ,
                required=name in default_args,
                mask_value=name in mask_args,
                logger=logger,
            )
            args[name] = arg if arg is not None else default_args[name]
    if logger:
        logger.section_end()
    return args


def write_github_outputs(
    kwargs: dict,
    to_env: bool = False,
    mask_args: tuple[str, ...] | list[str] = tuple(),
    logger: _Logger | None = None,
    log_title: str = "Write Step Outputs",
    log_title_env: str = "Write Environment Variables",
) -> None:

    def format_output(var_name, var_value) -> str | None:
        if isinstance(var_value, str):
            if "\n" in var_value:
                with open("/dev/urandom", "rb") as f:
                    random_bytes = f.read(15)
                random_delimeter = _base64.b64encode(random_bytes).decode("utf-8")
                return f"{var_name}<<{random_delimeter}\n{var_value}\n{random_delimeter}"
        elif isinstance(var_value, (dict, list, tuple, bool, int)):
            var_value = _json.dumps(var_value)
        else:
            return
        return f"{var_name}={var_value}"
    if logger:
        logger.section(log_title_env if to_env else log_title, group=True)
        logger.debug(message="Variables:", code=str(kwargs))
        logger.debug(message="Masked Arguments:", code=str(mask_args))
    output_name = 'environment' if to_env else 'step output'
    with open(_os.environ["GITHUB_ENV" if to_env else "GITHUB_OUTPUT"], "a") as fh:
        for idx, (name, value) in enumerate(kwargs.items()):
            name_formatted = name.replace("_", "-") if not to_env else name.upper()
            value_formatted = format_output(name_formatted, value)
            value_type_name = type(value).__name__
            if not value_formatted:
                err_msg = f"The corresponding input variable '{name}; has an invalid type '{value_type_name}'."
                err_title = f"Failed to write {output_name} variable '{name_formatted}'."
                if logger:
                    logger.critical(
                        title=err_title,
                        message=err_msg,
                        code=f"Value: {'**REDACTED**' if name in mask_args else value}",
                    )
                    logger.section_end()
                raise TypeError(f"{err_title} {err_msg}")
            print(value_formatted, file=fh)
            if logger:
                logger.info(
                    message=(
                        f"Output '{name}' (type: '{value_type_name}') "
                        f"successfully written to {output_name} variable '{name_formatted}'."
                    ),
                    code=f"Value: {'**REDACTED**' if name in mask_args else value}",
                )
    if logger:
        logger.section_end()
    return


def write_github_summary(
    content: str,
    logger: _Logger | None = None,
    log_title: str = "Write Job Summary",
) -> None:
    with open(_os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
        print(content, file=fh)
    if logger:
        logger.debug(
            title=log_title,
            message=(
                f"Successfully wrote job summary ({len(content)} chars) "
                f"to 'GITHUB_STEP_SUMMARY' environment variable."
            ),
            code=content,
        )
    return
