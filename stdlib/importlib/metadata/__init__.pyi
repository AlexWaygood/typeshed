import abc
import sys
from _typeshed import StrPath
from collections.abc import Iterable
from importlib.abc import MetaPathFinder
from typing import Any, ClassVar, NamedTuple, overload
from typing_extensions import Self

class _EntryPointBase(NamedTuple):
    name: str
    value: str
    group: str

class EntryPoint(_EntryPointBase):
    if sys.version_info >= (3, 11):
        def __init__(self, name: str, value: str, group: str) -> None: ...

    def load(self) -> Any: ...  # Callable[[], Any] or an importable module
    @property
    def extras(self) -> list[str]: ...
    if sys.version_info >= (3, 9):
        @property
        def module(self) -> str: ...
        @property
        def attr(self) -> str: ...
    if sys.version_info >= (3, 10):
        dist: ClassVar[Distribution | None]
        def matches(
            self,
            *,
            name: str = ...,
            value: str = ...,
            group: str = ...,
            module: str = ...,
            attr: str = ...,
            extras: list[str] = ...,
        ) -> bool: ...  # undocumented

    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...

if sys.version_info >= (3, 10):
    class EntryPoints(list[EntryPoint]):  # use as list is deprecated since 3.10
        # int argument is deprecated since 3.10
        def __getitem__(self, name: int | str) -> EntryPoint: ...  # type: ignore[override]
        def select(
            self,
            *,
            name: str = ...,
            value: str = ...,
            group: str = ...,
            module: str = ...,
            attr: str = ...,
            extras: list[str] = ...,
        ) -> EntryPoints: ...
        @property
        def names(self) -> set[str]: ...
        @property
        def groups(self) -> set[str]: ...

if sys.version_info >= (3, 10) and sys.version_info < (3, 12):
    class SelectableGroups(dict[str, EntryPoints]):  # use as dict is deprecated since 3.10
        @classmethod
        def load(cls, eps: Iterable[EntryPoint]) -> Self: ...
        @property
        def groups(self) -> set[str]: ...
        @property
        def names(self) -> set[str]: ...
        @overload
        def select(self) -> Self: ...  # type: ignore[misc]
        @overload
        def select(
            self,
            *,
            name: str = ...,
            value: str = ...,
            group: str = ...,
            module: str = ...,
            attr: str = ...,
            extras: list[str] = ...,
        ) -> EntryPoints: ...

class FileHash:
    mode: str
    value: str
    def __init__(self, spec: str) -> None: ...

class Distribution:
    @abc.abstractmethod
    def read_text(self, filename: str) -> str | None: ...
    @classmethod
    def from_name(cls, name: str) -> Distribution: ...
    @overload
    @classmethod
    def discover(cls, *, context: DistributionFinder.Context) -> Iterable[Distribution]: ...
    @overload
    @classmethod
    def discover(
        cls, *, context: None = None, name: str | None = ..., path: list[str] = ..., **kwargs: Any
    ) -> Iterable[Distribution]: ...
    @staticmethod
    def at(path: StrPath) -> PathDistribution: ...
    @property
    def metadata(self) -> Any: ...
    @property
    def entry_points(self) -> list[EntryPoint]: ...
    @property
    def version(self) -> str: ...
    @property
    def files(self) -> None: ...
    @property
    def requires(self) -> list[str] | None: ...
    if sys.version_info >= (3, 10):
        @property
        def name(self) -> str: ...

class DistributionFinder(MetaPathFinder):
    class Context:
        name: str | None
        def __init__(self, *, name: str | None = ..., path: list[str] = ..., **kwargs: Any) -> None: ...
        @property
        def path(self) -> list[str]: ...

    @abc.abstractmethod
    def find_distributions(self, context: DistributionFinder.Context = ...) -> Iterable[Distribution]: ...

class MetadataPathFinder(DistributionFinder):
    @classmethod
    def find_distributions(cls, context: DistributionFinder.Context = ...) -> Iterable[PathDistribution]: ...
    if sys.version_info >= (3, 10):
        # Yes, this is an instance method that has argumend named "cls"
        def invalidate_caches(cls) -> None: ...

class PathDistribution(Distribution):
    def __init__(self, path: str) -> None: ...
    def read_text(self, filename: StrPath) -> str: ...

def distribution(distribution_name: str) -> Distribution: ...
@overload
def distributions(*, context: DistributionFinder.Context) -> Iterable[Distribution]: ...
@overload
def distributions(
    *, context: None = None, name: str | None = ..., path: list[str] = ..., **kwargs: Any
) -> Iterable[Distribution]: ...
def entry_points(
    *, name: str = ..., value: str = ..., group: str = ..., module: str = ..., attr: str = ..., extras: list[str] = ...
) -> EntryPoints: ...
