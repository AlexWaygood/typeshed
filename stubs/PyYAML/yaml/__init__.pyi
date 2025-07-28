from collections.abc import Callable, Iterable, Iterator, Mapping
from re import Pattern
from typing import Any, TypeVar, overload

from . import resolver as resolver  # Help mypy a bit; this is implied by loader and dumper
from .constructor import BaseConstructor
from .cyaml import *
from .cyaml import _CLoader
from .dumper import *
from .dumper import _Inf
from .emitter import _WriteStream
from .error import *
from .events import *
from .loader import *
from .loader import _Loader
from .nodes import *
from .reader import _ReadStream
from .representer import BaseRepresenter
from .resolver import BaseResolver
from .tokens import *

_T = TypeVar("_T")
_Constructor = TypeVar("_Constructor", bound=BaseConstructor)
_Representer = TypeVar("_Representer", bound=BaseRepresenter)

__with_libyaml__: bool
__version__: str

def warnings(settings=None): ...
def scan(stream, Loader: type[_Loader | _CLoader] = ...):
    """
    Scan a YAML stream and produce scanning tokens.
    """

def parse(stream, Loader: type[_Loader | _CLoader] = ...):
    """
    Parse a YAML stream and produce parsing events.
    """

def compose(stream, Loader: type[_Loader | _CLoader] = ...):
    """
    Parse the first YAML document in a stream
    and produce the corresponding representation tree.
    """

def compose_all(stream, Loader: type[_Loader | _CLoader] = ...):
    """
    Parse all YAML documents in a stream
    and produce corresponding representation trees.
    """

def load(stream: _ReadStream, Loader: type[_Loader | _CLoader]) -> Any:
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """

def load_all(stream: _ReadStream, Loader: type[_Loader | _CLoader]) -> Iterator[Any]:
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """

def full_load(stream: _ReadStream) -> Any:
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve all tags except those known to be
    unsafe on untrusted input.
    """

def full_load_all(stream: _ReadStream) -> Iterator[Any]:
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve all tags except those known to be
    unsafe on untrusted input.
    """

def safe_load(stream: _ReadStream) -> Any:
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve only basic YAML tags. This is known
    to be safe for untrusted input.
    """

def safe_load_all(stream: _ReadStream) -> Iterator[Any]:
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve only basic YAML tags. This is known
    to be safe for untrusted input.
    """

def unsafe_load(stream: _ReadStream) -> Any:
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve all tags, even those known to be
    unsafe on untrusted input.
    """

def unsafe_load_all(stream: _ReadStream) -> Iterator[Any]:
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve all tags, even those known to be
    unsafe on untrusted input.
    """

def emit(
    events,
    stream: _WriteStream[Any] | None = None,
    Dumper=...,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
):
    """
    Emit YAML parsing events into a stream.
    If stream is None, return the produced string instead.
    """

@overload
def serialize_all(
    nodes,
    stream: _WriteStream[Any],
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> None:
    """
    Serialize a sequence of representation trees into a YAML stream.
    If stream is None, return the produced string instead.
    """

@overload
def serialize_all(
    nodes,
    stream: None = None,
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> str: ...
@overload
def serialize_all(
    nodes,
    stream: None = None,
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> bytes: ...
@overload
def serialize(
    node,
    stream: _WriteStream[Any],
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> None:
    """
    Serialize a representation tree into a YAML stream.
    If stream is None, return the produced string instead.
    """

@overload
def serialize(
    node,
    stream: None = None,
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> str: ...
@overload
def serialize(
    node,
    stream: None = None,
    Dumper=...,
    *,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
) -> bytes: ...
@overload
def dump_all(
    documents: Iterable[Any],
    stream: _WriteStream[Any],
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> None:
    """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """

@overload
def dump_all(
    documents: Iterable[Any],
    stream: None = None,
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> str: ...
@overload
def dump_all(
    documents: Iterable[Any],
    stream: None = None,
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> bytes: ...
@overload
def dump(
    data: Any,
    stream: _WriteStream[Any],
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> None:
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.
    """

@overload
def dump(
    data: Any,
    stream: None = None,
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> str: ...
@overload
def dump(
    data: Any,
    stream: None = None,
    Dumper=...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> bytes: ...
@overload
def safe_dump_all(
    documents: Iterable[Any],
    stream: _WriteStream[Any],
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> None:
    """
    Serialize a sequence of Python objects into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """

@overload
def safe_dump_all(
    documents: Iterable[Any],
    stream: None = None,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> str: ...
@overload
def safe_dump_all(
    documents: Iterable[Any],
    stream: None = None,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> bytes: ...
@overload
def safe_dump(
    data: Any,
    stream: _WriteStream[Any],
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> None:
    """
    Serialize a Python object into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """

@overload
def safe_dump(
    data: Any,
    stream: None = None,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> str: ...
@overload
def safe_dump(
    data: Any,
    stream: None = None,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | _Inf | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: str,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True,
) -> bytes: ...
def add_implicit_resolver(
    tag: str,
    regexp: Pattern[str],
    first: Iterable[Any] | None = None,
    Loader: type[BaseResolver] | None = None,
    Dumper: type[BaseResolver] = ...,
) -> None:
    """
    Add an implicit scalar detector.
    If an implicit scalar value matches the given regexp,
    the corresponding tag is assigned to the scalar.
    first is a sequence of possible initial characters or None.
    """

def add_path_resolver(
    tag: str,
    path: Iterable[Any],
    kind: type[Any] | None = None,
    Loader: type[BaseResolver] | None = None,
    Dumper: type[BaseResolver] = ...,
) -> None:
    """
    Add a path based resolver for the given tag.
    A path is a list of keys that forms a path
    to a node in the representation tree.
    Keys can be string values, integers, or None.
    """

@overload
def add_constructor(
    tag: str, constructor: Callable[[Loader | FullLoader | UnsafeLoader, Node], Any], Loader: None = None
) -> None:
    """
    Add a constructor for the given tag.
    Constructor is a function that accepts a Loader instance
    and a node object and produces the corresponding Python object.
    """

@overload
def add_constructor(tag: str, constructor: Callable[[_Constructor, Node], Any], Loader: type[_Constructor]) -> None: ...
@overload
def add_multi_constructor(
    tag_prefix: str, multi_constructor: Callable[[Loader | FullLoader | UnsafeLoader, str, Node], Any], Loader: None = None
) -> None:
    """
    Add a multi-constructor for the given tag prefix.
    Multi-constructor is called for a node if its tag starts with tag_prefix.
    Multi-constructor accepts a Loader instance, a tag suffix,
    and a node object and produces the corresponding Python object.
    """

@overload
def add_multi_constructor(
    tag_prefix: str, multi_constructor: Callable[[_Constructor, str, Node], Any], Loader: type[_Constructor]
) -> None: ...
@overload
def add_representer(data_type: type[_T], representer: Callable[[Dumper, _T], Node]) -> None:
    """
    Add a representer for the given type.
    Representer is a function accepting a Dumper instance
    and an instance of the given data type
    and producing the corresponding representation node.
    """

@overload
def add_representer(data_type: type[_T], representer: Callable[[_Representer, _T], Node], Dumper: type[_Representer]) -> None: ...
@overload
def add_multi_representer(data_type: type[_T], multi_representer: Callable[[Dumper, _T], Node]) -> None:
    """
    Add a representer for the given type.
    Multi-representer is a function accepting a Dumper instance
    and an instance of the given data type or subtype
    and producing the corresponding representation node.
    """

@overload
def add_multi_representer(
    data_type: type[_T], multi_representer: Callable[[_Representer, _T], Node], Dumper: type[_Representer]
) -> None: ...

class YAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """

    def __init__(cls, name, bases, kwds) -> None: ...

class YAMLObject(metaclass=YAMLObjectMetaclass):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """

    yaml_loader: Any
    yaml_dumper: Any
    yaml_tag: Any
    yaml_flow_style: Any
    @classmethod
    def from_yaml(cls, loader, node):
        """
        Convert a representation node to a Python object.
        """

    @classmethod
    def to_yaml(cls, dumper, data):
        """
        Convert a Python object to a representation node.
        """
