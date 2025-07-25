"""Logging and warning framework, predating Python's logging package"""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

class Logger:
    """
    An extended file type thing initially equivalent to sys.stderr
    You can add/remove file type things; it has a write method
    """

    def __init__(self) -> None: ...
    def add(self, fp) -> None:
        """add the file/string fp to the destinations"""

    def remove(self, fp) -> None:
        """remove the file/string fp from the destinations"""

    def write(self, text) -> None:
        """write text to all the destinations"""

    def __call__(self, text) -> None: ...

logger: Incomplete

class WarnOnce:
    uttered: Incomplete
    pfx: Incomplete
    enabled: int
    def __init__(self, kind: str = "Warn") -> None: ...
    def once(self, warning) -> None: ...
    def __call__(self, warning) -> None: ...

warnOnce: Incomplete
infoOnce: Incomplete
