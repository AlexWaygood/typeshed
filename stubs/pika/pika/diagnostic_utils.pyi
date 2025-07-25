"""
Diagnostic utilities
"""

from collections.abc import Callable
from logging import Logger
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

def create_log_exception_decorator(logger: Logger) -> Callable[[_F], _F]:
    """Create a decorator that logs and reraises any exceptions that escape
    the decorated function

    :param logging.Logger logger:
    :returns: the decorator
    :rtype: callable

    Usage example

    import logging

    from pika.diagnostics_utils import create_log_exception_decorator

    _log_exception = create_log_exception_decorator(logging.getLogger(__name__))

    @_log_exception
    def my_func_or_method():
        raise Exception('Oops!')

    """
