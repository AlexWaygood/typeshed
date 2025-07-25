from _typeshed import IdentityFunction
from collections.abc import Callable, Sequence
from logging import Logger
from typing import Any, TypeVar

_R = TypeVar("_R")

logging_logger: Logger

def retry_call(
    f: Callable[..., _R],
    fargs: Sequence[Any] | None = None,
    fkwargs: dict[str, Any] | None = None,
    exceptions: type[Exception] | tuple[type[Exception], ...] = ...,
    tries: int = -1,
    delay: float = 0,
    max_delay: float | None = None,
    backoff: float = 1,
    jitter: tuple[float, float] | float = 0,
    logger: Logger | None = ...,
) -> _R:
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """

def retry(
    exceptions: type[Exception] | tuple[type[Exception], ...] = ...,
    tries: int = -1,
    delay: float = 0,
    max_delay: float | None = None,
    backoff: float = 1,
    jitter: tuple[float, float] | float = 0,
    logger: Logger | None = ...,
) -> IdentityFunction:
    """Returns a retry decorator.

    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: a retry decorator.
    """
