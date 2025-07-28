from collections.abc import Callable
from typing import TypeVar
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_T = TypeVar("_T")

class RateLimitDecorator:
    """
    Rate limit decorator class.
    """

    def __init__(
        self, calls: int = 15, period: float = 900, clock: Callable[[], float] = ..., raise_on_limit: bool = True
    ) -> None:
        """
        Instantiate a RateLimitDecorator with some sensible defaults. By
        default the Twitter rate limiting window is respected (15 calls every
        15 minutes).

        :param int calls: Maximum function invocations allowed within a time period. Must be a number greater than 0.
        :param float period: An upper bound time period (in seconds) before the rate limit resets. Must be a number greater than 0.
        :param function clock: An optional function retuning the current time. This is used primarily for testing.
        :param bool raise_on_limit: A boolean allowing the caller to avoiding rasing an exception.
        """

    def __call__(self, func: Callable[_P, _T]) -> Callable[_P, _T]:
        """
        Return a wrapped function that prevents further function invocations if
        previously called within a specified period of time.

        :param function func: The function to decorate.
        :return: Decorated function.
        :rtype: function
        """

def sleep_and_retry(func: Callable[_P, _T]) -> Callable[_P, _T]:
    """
    Return a wrapped function that rescues rate limit exceptions, sleeping the
    current thread until rate limit resets.

    :param function func: The function to decorate.
    :return: Decorated function.
    :rtype: function
    """
