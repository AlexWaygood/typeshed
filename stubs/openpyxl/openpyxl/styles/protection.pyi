from typing import ClassVar, Literal

from openpyxl.descriptors.base import Bool, _ConvertibleToBool
from openpyxl.descriptors.serialisable import Serialisable

class Protection(Serialisable):
    """Protection options for use in styles."""

    tagname: ClassVar[str]
    locked: Bool[Literal[False]]
    hidden: Bool[Literal[False]]
    def __init__(self, locked: _ConvertibleToBool = True, hidden: _ConvertibleToBool = False) -> None: ...
