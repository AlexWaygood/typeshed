"""
RichText definition
"""

from collections.abc import Iterable
from typing import Literal, overload
from typing_extensions import Self

from openpyxl.cell.text import InlineFont
from openpyxl.descriptors import Strict, String, Typed
from openpyxl.descriptors.serialisable import _ChildSerialisableTreeElement
from openpyxl.xml.functions import Element

class TextBlock(Strict):
    """Represents text string in a specific format

    This class is used as part of constructing a rich text strings.
    """

    font: Typed[InlineFont, Literal[False]]
    text: String[Literal[False]]

    def __init__(self, font: InlineFont, text: str) -> None: ...
    def __eq__(self, other: TextBlock) -> bool: ...  # type: ignore[override]
    def to_tree(self) -> Element: ...

class CellRichText(list[str | TextBlock]):
    """Represents a rich text string.

    Initialize with a list made of pure strings or :class:`TextBlock` elements
    Can index object to access or modify individual rich text elements
    it also supports the + and += operators between rich text strings
    There are no user methods for this class

    operations which modify the string will generally call an optimization pass afterwards,
    that merges text blocks with identical formats, consecutive pure text strings,
    and remove empty strings and empty text blocks
    """

    @overload
    def __init__(self, args: list[str] | list[TextBlock] | list[str | TextBlock] | tuple[str | TextBlock, ...], /) -> None: ...
    @overload
    def __init__(self, *args: str | TextBlock) -> None: ...
    @classmethod
    def from_tree(cls, node: _ChildSerialisableTreeElement) -> Self: ...
    def __add__(self, arg: Iterable[str | TextBlock]) -> CellRichText: ...  # type: ignore[override]
    def append(self, arg: str | TextBlock) -> None: ...
    def extend(self, arg: Iterable[str | TextBlock]) -> None: ...
    def as_list(self) -> list[str]:
        """
        Returns a list of the strings contained.
        The main reason for this is to make editing easier.
        """

    def to_tree(self) -> Element:
        """
        Return the full XML representation
        """
