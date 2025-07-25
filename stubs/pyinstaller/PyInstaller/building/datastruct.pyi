# https://pyinstaller.org/en/stable/advanced-topics.html#the-toc-and-tree-classes
from collections.abc import Iterable, Sequence
from typing import ClassVar, Literal, SupportsIndex
from typing_extensions import LiteralString, Self, TypeAlias

_TypeCode: TypeAlias = Literal["DEPENDENCY", "SYMLINK", "DATA", "BINARY", "EXECUTABLE", "EXTENSION", "OPTION"]
_TOCTuple: TypeAlias = tuple[str, str | None, _TypeCode | None]

class TOC(list[_TOCTuple]):
    """
    TOC (Table of Contents) class is a list of tuples of the form (name, path, typecode).

    typecode    name                   path                        description
    --------------------------------------------------------------------------------------
    EXTENSION   Python internal name.  Full path name in build.    Extension module.
    PYSOURCE    Python internal name.  Full path name in build.    Script.
    PYMODULE    Python internal name.  Full path name in build.    Pure Python module (including __init__ modules).
    PYZ         Runtime name.          Full path name in build.    A .pyz archive (ZlibArchive data structure).
    PKG         Runtime name.          Full path name in build.    A .pkg archive (Carchive data structure).
    BINARY      Runtime name.          Full path name in build.    Shared library.
    DATA        Runtime name.          Full path name in build.    Arbitrary files.
    OPTION      The option.            Unused.                     Python runtime option (frozen into executable).

    A TOC contains various types of files. A TOC contains no duplicates and preserves order.
    PyInstaller uses TOC data type to collect necessary files bundle them into an executable.
    """

    filenames: set[str]
    def __init__(self, initlist: Iterable[_TOCTuple] | None = None) -> None: ...
    def append(self, entry: _TOCTuple) -> None: ...
    def insert(self, pos: SupportsIndex, entry: _TOCTuple) -> None: ...
    def __add__(self, other: Iterable[_TOCTuple]) -> TOC: ...  # type: ignore[override]
    def __radd__(self, other: Iterable[_TOCTuple]) -> TOC: ...
    def __iadd__(self, other: Iterable[_TOCTuple]) -> Self: ...  # type: ignore[override]
    def extend(self, other: Iterable[_TOCTuple]) -> None: ...
    def __sub__(self, other: Iterable[_TOCTuple]) -> TOC: ...
    def __rsub__(self, other: Iterable[_TOCTuple]) -> TOC: ...
    # slicing a TOC is not supported, but has a special case for slice(None, None, None)
    def __setitem__(self, key: int | slice, value: Iterable[_TOCTuple]) -> None: ...  # type: ignore[override]

class Target:
    invcnum: ClassVar[int]
    tocfilename: LiteralString
    tocbasename: LiteralString
    dependencies: list[_TOCTuple]
    def __init__(self) -> None: ...
    def __postinit__(self) -> None:
        """
        Check if the target need to be rebuild and if so, re-assemble.

        `__postinit__` is to be called at the end of `__init__` of every subclass of Target. `__init__` is meant to
        setup the parameters and `__postinit__` is checking if rebuild is required and in case calls `assemble()`
        """

class Tree(Target, list[_TOCTuple]):
    """
    This class is a way of creating a TOC (Table of Contents) list that describes some or all of the files within a
    directory.
    """

    root: str | None
    prefix: str | None
    excludes: Sequence[str]
    typecode: _TypeCode
    def __init__(
        self,
        root: str | None = None,
        prefix: str | None = None,
        excludes: Sequence[str] | None = None,
        typecode: _TypeCode = "DATA",
    ) -> None:
        """
        root
                The root of the tree (on the build system).
        prefix
                Optional prefix to the names of the target system.
        excludes
                A list of names to exclude. Two forms are allowed:

                    name
                        Files with this basename will be excluded (do not include the path).
                    *.ext
                        Any file with the given extension will be excluded.
        typecode
                The typecode to be used for all files found in this tree. See the TOC class for for information about
                the typcodes.
        """

    def assemble(self) -> None: ...

def normalize_toc(toc: Iterable[_TOCTuple]) -> list[_TOCTuple]: ...
def normalize_pyz_toc(toc: Iterable[_TOCTuple]) -> list[_TOCTuple]: ...
def toc_process_symbolic_links(toc: Iterable[_TOCTuple]) -> list[_TOCTuple]:
    """
    Process TOC entries and replace entries whose files are symbolic links with SYMLINK entries (provided original file
    is also being collected).
    """
