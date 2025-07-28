from _typeshed import Incomplete, Unused
from collections.abc import Generator
from typing import ClassVar, Literal, TypeVar, overload
from zipfile import ZipFile

from openpyxl.descriptors.base import Alias, String
from openpyxl.descriptors.container import ElementList
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.pivot.cache import CacheDefinition
from openpyxl.pivot.record import RecordList
from openpyxl.pivot.table import TableDefinition

_SerialisableT = TypeVar("_SerialisableT", bound=Serialisable)
_SerialisableRelTypeT = TypeVar("_SerialisableRelTypeT", bound=CacheDefinition | RecordList | TableDefinition)

class Relationship(Serialisable):
    """Represents many kinds of relationships."""

    tagname: ClassVar[str]
    Type: String[Literal[False]]
    Target: String[Literal[False]]
    target: Alias
    TargetMode: String[Literal[True]]
    Id: String[Literal[True]]
    id: Alias
    @overload
    def __init__(
        self, Id: str, Type: Unused = None, *, type: str, Target: str | None = None, TargetMode: str | None = None
    ) -> None:
        """
        `type` can be used as a shorthand with the default relationships namespace
        otherwise the `Type` must be a fully qualified URL
        """

    @overload
    def __init__(self, Id: str, Type: Unused, type: str, Target: str | None = None, TargetMode: str | None = None) -> None: ...
    @overload
    def __init__(
        self, Id: str, Type: str, type: None = None, Target: str | None = None, TargetMode: str | None = None
    ) -> None: ...

class RelationshipList(ElementList[Relationship]):
    expected_type: type[Relationship]
    def find(self, content_type: str) -> Generator[Relationship, None, None]:
        """
        Find relationships by content-type
        NB. these content-types namespaced objects and different to the MIME-types
        in the package manifest :-(
        """

    def get(self, key: str) -> Relationship: ...
    def to_dict(self) -> dict[Incomplete, Relationship]:
        """Return a dictionary of relations keyed by id"""

def get_rels_path(path):
    """
    Convert relative path to absolutes that can be loaded from a zip
    archive.
    The path to be passed in is that of containing object (workbook,
    worksheet, etc.)
    """

def get_dependents(archive: ZipFile, filename: str) -> RelationshipList:
    """
    Normalise dependency file paths to absolute ones

    Relative paths are relative to parent object
    """

# If `id` is None, `cls` needs to have ClassVar `rel_type`.
# The `deps` attribute used at runtime is for internal use immediately after the return.
# `cls` cannot be None
@overload
def get_rel(
    archive: ZipFile, deps: RelationshipList, id: None = None, *, cls: type[_SerialisableRelTypeT]
) -> _SerialisableRelTypeT | None:
    """
    Get related object based on id or rel_type
    """

@overload
def get_rel(
    archive: ZipFile, deps: RelationshipList, id: None, cls: type[_SerialisableRelTypeT]
) -> _SerialisableRelTypeT | None: ...
@overload
def get_rel(archive: ZipFile, deps: RelationshipList, id: str, cls: type[_SerialisableT]) -> _SerialisableT: ...
