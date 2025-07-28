from _typeshed import SupportsRead, SupportsWrite
from collections.abc import Callable
from typing import Any, Final

__version__: Final[str]

def encode(
    obj: Any,
    ensure_ascii: bool = ...,
    double_precision: int = ...,
    encode_html_chars: bool = ...,
    escape_forward_slashes: bool = ...,
    sort_keys: bool = ...,
    indent: int = ...,
    allow_nan: bool = ...,
    reject_bytes: bool = ...,
    default: Callable[[Any], Any] | None = None,  # Specify how to serialize arbitrary types
    separators: tuple[str, str] | None = None,
) -> str:
    """Converts arbitrary object recursively into JSON. Use ensure_ascii=false to output UTF-8. Set encode_html_chars=True to encode < > & as unicode escape sequences. Set escape_forward_slashes=False to prevent escaping / characters.Set allow_nan=False to raise an exception when NaN or Infinity would be serialized.Set reject_bytes=True to raise TypeError on bytes."""

def dumps(
    obj: Any,
    ensure_ascii: bool = ...,
    double_precision: int = ...,
    encode_html_chars: bool = ...,
    escape_forward_slashes: bool = ...,
    sort_keys: bool = ...,
    indent: int = ...,
    allow_nan: bool = ...,
    reject_bytes: bool = ...,
    default: Callable[[Any], Any] | None = None,  # Specify how to serialize arbitrary types
    separators: tuple[str, str] | None = None,
) -> str:
    """Converts arbitrary object recursively into JSON. Use ensure_ascii=false to output UTF-8. Set encode_html_chars=True to encode < > & as unicode escape sequences. Set escape_forward_slashes=False to prevent escaping / characters.Set allow_nan=False to raise an exception when NaN or Infinity would be serialized.Set reject_bytes=True to raise TypeError on bytes."""

def dump(
    obj: Any,
    fp: SupportsWrite[str],
    *,
    ensure_ascii: bool = ...,
    double_precision: int = ...,
    encode_html_chars: bool = ...,
    escape_forward_slashes: bool = ...,
    sort_keys: bool = ...,
    indent: int = ...,
    allow_nan: bool = ...,
    reject_bytes: bool = ...,
    default: Callable[[Any], Any] | None = None,  # Specify how to serialize arbitrary types
    separators: tuple[str, str] | None = None,
) -> None:
    """Converts arbitrary object recursively into JSON file. Use ensure_ascii=false to output UTF-8. Set encode_html_chars=True to encode < > & as unicode escape sequences. Set escape_forward_slashes=False to prevent escaping / characters.Set allow_nan=False to raise an exception when NaN or Infinity would be serialized.Set reject_bytes=True to raise TypeError on bytes."""

def decode(s: str | bytes | bytearray, precise_float: bool = ...) -> Any:
    """Converts JSON as string to dict object structure."""

def loads(s: str | bytes | bytearray, precise_float: bool = ...) -> Any:
    """Converts JSON as string to dict object structure."""

def load(fp: SupportsRead[str | bytes | bytearray], precise_float: bool = ...) -> Any:
    """Converts JSON as file to dict object structure."""

class JSONDecodeError(ValueError): ...
