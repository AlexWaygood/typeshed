from _typeshed import SupportsDunderGT, SupportsDunderLT, SupportsRead
from collections.abc import Iterable, Mapping, Sequence
from re import Pattern
from typing import Any, Final, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from Xlib.display import Display
from Xlib.support.lock import _DummyLock

_T = TypeVar("_T")
_T_contra = TypeVar("_T_contra", contravariant=True)

_DB: TypeAlias = dict[str, tuple[_DB, ...]]
# A recursive type can be a bit annoying due to dict invariance,
# so this is a slightly less precise version of the _DB alias for parameter annotations
_DB_Param: TypeAlias = dict[str, Any]

class _SupportsComparisons(SupportsDunderLT[_T_contra], SupportsDunderGT[_T_contra], Protocol[_T_contra]): ...

comment_re: Final[Pattern[str]]
resource_spec_re: Final[Pattern[str]]
value_escape_re: Final[Pattern[str]]
resource_parts_re: Final[Pattern[str]]
NAME_MATCH: Final = 0
CLASS_MATCH: Final = 2
WILD_MATCH: Final = 4
MATCH_SKIP: Final = 6

class OptionError(Exception): ...

class ResourceDB:
    db: _DB
    lock: _DummyLock
    def __init__(
        self,
        file: bytes | SupportsRead[str] | None = None,
        string: str | None = None,
        resources: Iterable[tuple[str, object]] | None = None,
    ) -> None: ...
    def insert_file(self, file: bytes | SupportsRead[str]) -> None:
        """insert_file(file)

        Load resources entries from FILE, and insert them into the
        database.  FILE can be a filename (a string)or a file object.

        """

    def insert_string(self, data: str) -> None:
        """insert_string(data)

        Insert the resources entries in the string DATA into the
        database.

        """

    def insert_resources(self, resources: Iterable[tuple[str, object]]) -> None:
        """insert_resources(resources)

        Insert all resources entries in the list RESOURCES into the
        database.  Each element in RESOURCES should be a tuple:

          (resource, value)

        Where RESOURCE is a string and VALUE can be any Python value.

        """

    def insert(self, resource: str, value: object) -> None:
        """insert(resource, value)

        Insert a resource entry into the database.  RESOURCE is a
        string and VALUE can be any Python value.

        """

    def __getitem__(self, keys_tuple: tuple[str, str]) -> Any:
        """db[name, class]

        Return the value matching the resource identified by NAME and
        CLASS.  If no match is found, KeyError is raised.
        """

    @overload
    def get(self, res: str, cls: str, default: None = None) -> Any:
        """get(name, class [, default])

        Return the value matching the resource identified by NAME and
        CLASS.  If no match is found, DEFAULT is returned, or None if
        DEFAULT isn't specified.

        """

    @overload
    def get(self, res: str, cls: str, default: _T) -> _T: ...
    def update(self, db: ResourceDB) -> None:
        """update(db)

        Update this database with all resources entries in the resource
        database DB.

        """

    def output(self) -> str:
        """output()

        Return the resource database in text representation.
        """

    def getopt(self, name: str, argv: Sequence[str], opts: Mapping[str, Option]) -> Sequence[str]:
        """getopt(name, argv, opts)

        Parse X command line options, inserting the recognised options
        into the resource database.

        NAME is the application name, and will be prepended to all
        specifiers.  ARGV is the list of command line arguments,
        typically sys.argv[1:].

        OPTS is a mapping of options to resource specifiers.  The key is
        the option flag (with leading -), and the value is an instance of
        some Option subclass:

        NoArg(specifier, value): set resource to value.
        IsArg(specifier):        set resource to option itself
        SepArg(specifier):       value is next argument
        ResArg:                  resource and value in next argument
        SkipArg:                 ignore this option and next argument
        SkipLine:                ignore rest of arguments
        SkipNArgs(count):        ignore this option and count arguments

        The remaining, non-option, oparguments is returned.

        rdb.OptionError is raised if there is an error in the argument list.
        """

def bin_insert(list: list[_SupportsComparisons[_T]], element: _SupportsComparisons[_T]) -> None:
    """bin_insert(list, element)

    Insert ELEMENT into LIST.  LIST must be sorted, and ELEMENT will
    be inserted to that LIST remains sorted.  If LIST already contains
    ELEMENT, it will not be duplicated.

    """

def update_db(dest: _DB_Param, src: _DB_Param) -> None: ...
def copy_group(group: tuple[_DB_Param, ...]) -> tuple[_DB, ...]: ...
def copy_db(db: _DB_Param) -> _DB: ...
def output_db(prefix: str, db: _DB_Param) -> str: ...
def output_escape(value: object) -> str: ...

class Option:
    def parse(self, name: str, db: ResourceDB, args: Sequence[_T]) -> Sequence[_T]: ...

class NoArg(Option):
    """Value is provided to constructor."""

    specifier: str
    value: object
    def __init__(self, specifier: str, value: object) -> None: ...

class IsArg(Option):
    """Value is the option string itself."""

    specifier: str
    def __init__(self, specifier: str) -> None: ...

class SepArg(Option):
    """Value is the next argument."""

    specifier: str
    def __init__(self, specifier: str) -> None: ...

class ResArgClass(Option):
    """Resource and value in the next argument."""

    def parse(self, name: str, db: ResourceDB, args: Sequence[str]) -> Sequence[str]: ...  # type: ignore[override]

ResArg: ResArgClass

class SkipArgClass(Option):
    """Ignore this option and next argument."""

SkipArg: SkipArgClass

class SkipLineClass(Option):
    """Ignore rest of the arguments."""

SkipLine: SkipLineClass

class SkipNArgs(Option):
    """Ignore this option and the next COUNT arguments."""

    count: int
    def __init__(self, count: int) -> None: ...

def get_display_opts(options: Mapping[str, Option], argv: Sequence[str] = ...) -> tuple[Display, str, ResourceDB, Sequence[str]]:
    """display, name, db, args = get_display_opts(options, [argv])

    Parse X OPTIONS from ARGV (or sys.argv if not provided).

    Connect to the display specified by a *.display resource if one is
    set, or to the default X display otherwise.  Extract the
    RESOURCE_MANAGER property and insert all resources from ARGV.

    The four return values are:
      DISPLAY -- the display object
      NAME    -- the application name (the filname of ARGV[0])
      DB      -- the created resource database
      ARGS    -- any remaining arguments
    """

stdopts: Final[dict[str, SepArg | NoArg | ResArgClass]]
