from _typeshed import SupportsWrite
from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import Any, Generic, TypeVar, overload

_MappingT = TypeVar("_MappingT", bound=Mapping[str, Any])

def dump(o: _MappingT, f: SupportsWrite[str], encoder: TomlEncoder[_MappingT] | None = None) -> str:
    """Writes out dict as toml to a file

    Args:
        o: Object to dump into toml
        f: File descriptor where the toml should be stored
        encoder: The ``TomlEncoder`` to use for constructing the output string

    Returns:
        String containing the toml corresponding to dictionary

    Raises:
        TypeError: When anything other than file descriptor is passed
    """

def dumps(o: _MappingT, encoder: TomlEncoder[_MappingT] | None = None) -> str:
    """Stringifies input dict as toml

        Args:
            o: Object to dump into toml
            encoder: The ``TomlEncoder`` to use for constructing the output string

        Returns:
            String containing the toml corresponding to dict

        Examples:
            ```python
            >>> import toml
            >>> output = {
            ... 'a': "I'm a string",
            ... 'b': ["I'm", "a", "list"],
            ... 'c': 2400
            ... }
            >>> toml.dumps(output)
            'a = "I'm a string"
    b = [ "I'm", "a", "list",]
    c = 2400
    '
            ```
    """

class TomlEncoder(Generic[_MappingT]):
    _dict: type[_MappingT]
    preserve: bool
    dump_funcs: MutableMapping[type[Any], Callable[[Any], str]]
    @overload
    def __init__(self, _dict: type[_MappingT], preserve: bool = False) -> None: ...
    @overload
    def __init__(self: TomlEncoder[dict[str, Any]], _dict: type[dict[str, Any]] = ..., preserve: bool = False) -> None: ...
    def get_empty_table(self) -> _MappingT: ...
    def dump_list(self, v: Iterable[Any]) -> str: ...
    def dump_inline_table(self, section: dict[str, Any] | Any) -> str:
        """Preserve inline table in its compact syntax instead of expanding
        into subsection.

        https://github.com/toml-lang/toml#user-content-inline-table
        """

    def dump_value(self, v: Any) -> str: ...
    def dump_sections(self, o: _MappingT, sup: str) -> tuple[str, _MappingT]: ...

class TomlPreserveInlineDictEncoder(TomlEncoder[_MappingT]):
    @overload
    def __init__(self, _dict: type[_MappingT]) -> None: ...
    @overload
    def __init__(self: TomlPreserveInlineDictEncoder[dict[str, Any]], _dict: type[dict[str, Any]] = ...) -> None: ...

class TomlArraySeparatorEncoder(TomlEncoder[_MappingT]):
    separator: str
    @overload
    def __init__(self, _dict: type[_MappingT], preserve: bool = False, separator: str = ",") -> None: ...
    @overload
    def __init__(
        self: TomlArraySeparatorEncoder[dict[str, Any]],
        _dict: type[dict[str, Any]] = ...,
        preserve: bool = False,
        separator: str = ",",
    ) -> None: ...
    def dump_list(self, v: Iterable[Any]) -> str: ...

class TomlNumpyEncoder(TomlEncoder[_MappingT]): ...
class TomlPreserveCommentEncoder(TomlEncoder[_MappingT]): ...
class TomlPathlibEncoder(TomlEncoder[_MappingT]): ...
