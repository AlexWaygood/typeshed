from _typeshed import Incomplete
from typing import NamedTuple

__all__ = ["RL_Codecs"]

class StdCodecData(NamedTuple):
    """StdCodecData(exceptions, rexceptions)"""

    exceptions: Incomplete
    rexceptions: Incomplete

class ExtCodecData(NamedTuple):
    """ExtCodecData(baseName, exceptions, rexceptions)"""

    baseName: Incomplete
    exceptions: Incomplete
    rexceptions: Incomplete

class RL_Codecs:
    def __init__(self) -> None: ...
    @staticmethod
    def register() -> None: ...
    @staticmethod
    def add_dynamic_codec(name, exceptions, rexceptions) -> None: ...
    @staticmethod
    def remove_dynamic_codec(name) -> None: ...
    @staticmethod
    def reset_dynamic_codecs() -> None: ...
