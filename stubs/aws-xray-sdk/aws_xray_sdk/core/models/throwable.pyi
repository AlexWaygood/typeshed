from _typeshed import Incomplete
from logging import Logger
from traceback import StackSummary
from typing import TypedDict, type_check_only

@type_check_only
class _StackInfo(TypedDict):
    path: str
    line: int
    label: str

log: Logger

class Throwable:
    """
    An object recording exception infomation under trace entity
    `cause` section. The information includes the stack trace,
    working directory and message from the original exception.
    """

    id: str
    message: str
    type: str
    remote: bool
    stack: list[_StackInfo] | None
    def __init__(self, exception: Exception, stack: StackSummary, remote: bool = False) -> None:
        """
        :param Exception exception: the catched exception.
        :param list stack: the formatted stack trace gathered
            through `traceback` module.
        :param bool remote: If False it means it's a client error
            instead of a downstream service.
        """

    def to_dict(self) -> dict[str, Incomplete]:
        """
        Convert Throwable object to dict with required properties that
        have non-empty values.
        """
