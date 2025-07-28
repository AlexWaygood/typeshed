"""
This package contains Docutils Reader modules.
"""

from typing import Any, ClassVar, Final, Generic, TypeVar

from docutils import Component, nodes
from docutils.frontend import Values
from docutils.io import Input
from docutils.parsers import Parser
from docutils.transforms import Transform

_S = TypeVar("_S")

__docformat__: Final = "reStructuredText"

class Reader(Component, Generic[_S]):
    """
    Abstract base class for docutils Readers.

    Each reader module or package must export a subclass also called 'Reader'.

    The two steps of a Reader's responsibility are to read data from the
    source Input object and parse the data with the Parser object.
    Call `read()` to process a document.
    """

    component_type: ClassVar[str]
    config_section: ClassVar[str]
    def get_transforms(self) -> list[type[Transform]]: ...
    def __init__(self, parser: Parser | None = None, parser_name: str | None = None) -> None:
        """
        Initialize the Reader instance.

        Several instance attributes are defined with dummy initial values.
        Subclasses may use these attributes as they wish.
        """
    parser: Parser | None
    source: Input[_S] | None
    input: str | None
    def set_parser(self, parser_name: str) -> None:
        """Set `self.parser` by name."""
    settings: Values
    def read(self, source: Input[_S], parser: Parser, settings: Values) -> nodes.document: ...
    document: nodes.document
    def parse(self) -> None:
        """Parse `self.input` into a document tree."""

    def new_document(self) -> nodes.document:
        """Create and return a new empty document tree (root node)."""

class ReReader(Reader[_S]):
    """
    A reader which rereads an existing document tree (e.g. a
    deserializer).

    Often used in conjunction with `writers.UnfilteredWriter`.
    """

    def get_transforms(self) -> list[type[Transform]]: ...

def get_reader_class(reader_name: str) -> type[Reader[Any]]:
    """Return the Reader class from the `reader_name` module."""
