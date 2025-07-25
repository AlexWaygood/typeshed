from abc import abstractmethod
from collections.abc import Iterable
from threading import Lock
from typing import Any, ClassVar, Literal, Protocol, TypeVar, type_check_only
from typing_extensions import Self

from fanstatic.compiler import Compiler, Minifier
from fanstatic.core import Library
from fanstatic.injector import InjectorPlugin

# Used to be pkg_resources.EntryPoint, but any EntryPoint-like class with a `load` method works
@type_check_only
class _EntryPoint(Protocol):
    def load(self) -> Any: ...  # Can be any attribute in the module

@type_check_only
class _HasName(Protocol):
    @property
    def name(self) -> str: ...

_NamedT = TypeVar("_NamedT", bound=_HasName)

prepare_lock: Lock

class Registry(dict[str, _NamedT]):
    @property
    @abstractmethod
    def ENTRY_POINT(self) -> str:
        """The type of the NotImplemented singleton."""

    def __init__(self, items: Iterable[_NamedT] = ()) -> None: ...
    def add(self, item: _NamedT) -> None: ...
    def load_items_from_entry_points(self) -> None: ...
    def make_item_from_entry_point(self, entry_point: _EntryPoint) -> Any: ...
    @classmethod
    def instance(cls) -> Self: ...

class LibraryRegistry(Registry[Library]):
    """A dictionary-like registry of libraries.

    This is a dictionary that maintains libraries. A value is a
    :py:class:`Library` instance, and a key is its library ``name``.

    Normally there is only a single global LibraryRegistry,
    obtained by calling ``get_library_registry()``.

    :param libraries: a sequence of libraries
    """

    ENTRY_POINT: ClassVar[Literal["fanstatic.libraries"]]
    prepared: bool
    def prepare(self) -> None: ...

get_library_registry = LibraryRegistry.instance

class CompilerRegistry(Registry[Compiler]):
    ENTRY_POINT: ClassVar[Literal["fanstatic.compilers"]]

class MinifierRegistry(Registry[Minifier]):
    ENTRY_POINT: ClassVar[Literal["fanstatic.minifiers"]]

class InjectorRegistry(Registry[InjectorPlugin]):
    ENTRY_POINT: ClassVar[Literal["fanstatic.injectors"]]
