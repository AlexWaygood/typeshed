"""
This module contains various contacts, classes and functions which get referenced and used
throughout the code base.
"""

import sys
from collections.abc import Iterator
from re import Pattern
from typing import Final, Generic, TypedDict, TypeVar, overload

from markdown.core import Markdown

_T = TypeVar("_T")

BLOCK_LEVEL_ELEMENTS: Final[list[str]]
STX: Final[str]
ETX: Final[str]
INLINE_PLACEHOLDER_PREFIX: Final[str]
INLINE_PLACEHOLDER: Final[str]
INLINE_PLACEHOLDER_RE: Final[Pattern[str]]
AMP_SUBSTITUTE: Final[str]
HTML_PLACEHOLDER: Final[str]
HTML_PLACEHOLDER_RE: Final[Pattern[str]]
TAG_PLACEHOLDER: Final[str]
RTL_BIDI_RANGES: Final[tuple[tuple[str, str], tuple[str, str]]]

if sys.version_info >= (3, 10):
    from importlib import metadata
    def get_installed_extensions() -> metadata.EntryPoints:
        """Return all entry_points in the `markdown.extensions` group."""

else:
    def get_installed_extensions(): ...

def deprecated(message: str, stacklevel: int = 2):
    """
    Raise a [`DeprecationWarning`][] when wrapped function/method is called.

    Usage:

    ```python
    @deprecated("This method will be removed in version X; use Y instead.")
    def some_method():
        pass
    ```
    """

@overload
def parseBoolValue(value: str) -> bool:
    """Parses a string representing a boolean value. If parsing was successful,
    returns `True` or `False`. If `preserve_none=True`, returns `True`, `False`,
    or `None`. If parsing was not successful, raises `ValueError`, or, if
    `fail_on_errors=False`, returns `None`.
    """

@overload
def parseBoolValue(value: str | None, fail_on_errors: bool = True, preserve_none: bool = False) -> bool | None: ...
def code_escape(text: str) -> str:
    """HTML escape a string of code."""

def nearing_recursion_limit() -> bool:
    """Return true if current stack depth is within 100 of maximum limit."""

class AtomicString(str):
    """A string which should not be further processed."""

class Processor:
    """The base class for all processors.

    Attributes:
        Processor.md: The `Markdown` instance passed in an initialization.

    Arguments:
        md: The `Markdown` instance this processor is a part of.

    """

    md: Markdown
    def __init__(self, md: Markdown | None = None) -> None: ...

class _TagData(TypedDict):
    tag: str
    attrs: dict[str, str]
    left_index: int
    right_index: int

class HtmlStash:
    """
    This class is used for stashing HTML objects that we extract
    in the beginning and replace with place-holders.
    """

    html_counter: int
    rawHtmlBlocks: list[str]
    tag_counter: int
    tag_data: list[_TagData]
    def __init__(self) -> None:
        """Create an `HtmlStash`."""

    def store(self, html: str) -> str:
        """
        Saves an HTML segment for later reinsertion.  Returns a
        placeholder string that needs to be inserted into the
        document.

        Keyword arguments:
            html: An html segment.

        Returns:
            A placeholder string.

        """

    def reset(self) -> None:
        """Clear the stash."""

    def get_placeholder(self, key: int) -> str: ...
    def store_tag(self, tag: str, attrs: dict[str, str], left_index: int, right_index: int) -> str:
        """Store tag data and return a placeholder."""

class Registry(Generic[_T]):
    """
    A priority sorted registry.

    A `Registry` instance provides two public methods to alter the data of the
    registry: `register` and `deregister`. Use `register` to add items and
    `deregister` to remove items. See each method for specifics.

    When registering an item, a "name" and a "priority" must be provided. All
    items are automatically sorted by "priority" from highest to lowest. The
    "name" is used to remove ("deregister") and get items.

    A `Registry` instance it like a list (which maintains order) when reading
    data. You may iterate over the items, get an item and get a count (length)
    of all items. You may also check that the registry contains an item.

    When getting an item you may use either the index of the item or the
    string-based "name". For example:

        registry = Registry()
        registry.register(SomeItem(), 'itemname', 20)
        # Get the item by index
        item = registry[0]
        # Get the item by name
        item = registry['itemname']

    When checking that the registry contains an item, you may use either the
    string-based "name", or a reference to the actual item. For example:

        someitem = SomeItem()
        registry.register(someitem, 'itemname', 20)
        # Contains the name
        assert 'itemname' in registry
        # Contains the item instance
        assert someitem in registry

    The method `get_index_for_name` is also available to obtain the index of
    an item using that item's assigned "name".
    """

    def __init__(self) -> None: ...
    def __contains__(self, item: str | _T) -> bool: ...
    def __iter__(self) -> Iterator[_T]: ...
    @overload
    def __getitem__(self, key: slice) -> Registry[_T]: ...
    @overload
    def __getitem__(self, key: str | int) -> _T: ...
    def __len__(self) -> int: ...
    def get_index_for_name(self, name: str) -> int:
        """
        Return the index of the given name.
        """

    def register(self, item: _T, name: str, priority: float) -> None:
        """
        Add an item to the registry with the given name and priority.

        Arguments:
            item: The item being registered.
            name: A string used to reference the item.
            priority: An integer or float used to sort against all items.

        If an item is registered with a "name" which already exists, the
        existing item is replaced with the new item. Treat carefully as the
        old item is lost with no way to recover it. The new item will be
        sorted according to its priority and will **not** retain the position
        of the old item.
        """

    def deregister(self, name: str, strict: bool = True) -> None:
        """
        Remove an item from the registry.

        Set `strict=False` to fail silently. Otherwise a [`ValueError`][] is raised for an unknown `name`.
        """
