from _typeshed import SupportsRead
from collections.abc import Callable, MutableMapping
from pathlib import PurePath
from re import Pattern
from typing import Any, Generic, TypeVar, overload
from typing_extensions import TypeAlias

_MutableMappingT = TypeVar("_MutableMappingT", bound=MutableMapping[str, Any])
_PathLike: TypeAlias = str | bytes | PurePath

FNFError = FileNotFoundError
TIME_RE: Pattern[str]

class TomlDecodeError(ValueError):
    """Base toml Exception / Error."""

    msg: str
    doc: str
    pos: int
    lineno: int
    colno: int
    def __init__(self, msg: str, doc: str, pos: int) -> None: ...

class CommentValue:
    val: Any
    comment: str
    def __init__(self, val: Any, comment: str, beginline: bool, _dict: type[MutableMapping[str, Any]]) -> None: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def dump(self, dump_value_func: Callable[[Any], str]) -> str: ...

@overload
def load(
    f: _PathLike | list[Any] | SupportsRead[str],  # list[_PathLike] is invariance
    _dict: type[_MutableMappingT],
    decoder: TomlDecoder[_MutableMappingT] | None = None,
) -> _MutableMappingT:
    """Parses named file or files as toml and returns a dictionary

    Args:
        f: Path to the file to open, array of files to read into single dict
           or a file descriptor
        _dict: (optional) Specifies the class of the returned toml dictionary
        decoder: The decoder to use

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError -- When f is invalid type
        TomlDecodeError: Error while decoding toml
        IOError / FileNotFoundError -- When an array with no valid (existing)
        (Python 2 / Python 3)          file paths is passed
    """

@overload
def load(
    f: _PathLike | list[Any] | SupportsRead[str],  # list[_PathLike] is invariance
    _dict: type[dict[str, Any]] = ...,
    decoder: TomlDecoder[dict[str, Any]] | None = None,
) -> dict[str, Any]: ...
@overload
def loads(s: str, _dict: type[_MutableMappingT], decoder: TomlDecoder[_MutableMappingT] | None = None) -> _MutableMappingT:
    """Parses string as toml

    Args:
        s: String to be parsed
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError: When a non-string is passed
        TomlDecodeError: Error while decoding toml
    """

@overload
def loads(s: str, _dict: type[dict[str, Any]] = ..., decoder: TomlDecoder[dict[str, Any]] | None = None) -> dict[str, Any]: ...

class InlineTableDict:
    """Sentinel subclass of dict for inline tables."""

class TomlDecoder(Generic[_MutableMappingT]):
    _dict: type[_MutableMappingT]
    @overload
    def __init__(self, _dict: type[_MutableMappingT]) -> None: ...
    @overload
    def __init__(self: TomlDecoder[dict[str, Any]], _dict: type[dict[str, Any]] = ...) -> None: ...
    def get_empty_table(self) -> _MutableMappingT: ...
    def get_empty_inline_table(self) -> InlineTableDict: ...  # incomplete python/typing#213
    def load_inline_object(
        self, line: str, currentlevel: _MutableMappingT, multikey: bool = False, multibackslash: bool = False
    ) -> None: ...
    def load_line(
        self, line: str, currentlevel: _MutableMappingT, multikey: bool | None, multibackslash: bool
    ) -> tuple[bool | None, str, bool] | None: ...
    def load_value(self, v: str, strictly_valid: bool = True) -> tuple[Any, str]: ...
    def bounded_string(self, s: str) -> bool: ...
    def load_array(self, a: str) -> list[Any]: ...
    def preserve_comment(self, line_no: int, key: str, comment: str, beginline: bool) -> None: ...
    def embed_comments(self, idx: int, currentlevel: _MutableMappingT) -> None: ...

class TomlPreserveCommentDecoder(TomlDecoder[_MutableMappingT]):
    saved_comments: dict[int, tuple[str, str, bool]]
