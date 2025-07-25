"""
File manifest
"""

from _typeshed import Incomplete
from collections.abc import Generator
from typing import ClassVar, Final, Literal

from openpyxl.descriptors.base import String
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.xml.functions import Element

mimetypes: Incomplete

class FileExtension(Serialisable):
    tagname: ClassVar[str]
    Extension: String[Literal[False]]
    ContentType: String[Literal[False]]
    def __init__(self, Extension: str, ContentType: str) -> None: ...

class Override(Serialisable):
    tagname: ClassVar[str]
    PartName: String[Literal[False]]
    ContentType: String[Literal[False]]
    def __init__(self, PartName: str, ContentType: str) -> None: ...

DEFAULT_TYPES: Final[list[FileExtension]]
DEFAULT_OVERRIDE: Final[list[Override]]

class Manifest(Serialisable):
    tagname: ClassVar[str]
    Default: Incomplete
    Override: Incomplete
    path: str
    __elements__: ClassVar[tuple[str, ...]]
    def __init__(self, Default=(), Override=()) -> None: ...
    @property
    def filenames(self) -> list[str]: ...
    @property
    def extensions(self) -> list[tuple[str, str]]:
        """
        Map content types to file extensions
        Skip parts without extensions
        """

    def to_tree(self) -> Element:  # type: ignore[override]
        """
        Custom serialisation method to allow setting a default namespace
        """

    def __contains__(self, content_type: str) -> bool:
        """
        Check whether a particular content type is contained
        """

    def find(self, content_type):
        """
        Find specific content-type
        """

    def findall(self, content_type) -> Generator[Incomplete, None, None]:
        """
        Find all elements of a specific content-type
        """

    def append(self, obj) -> None:
        """
        Add content object to the package manifest
        # needs a contract...
        """
