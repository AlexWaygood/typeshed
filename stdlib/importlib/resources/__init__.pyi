import sys
from collections.abc import Iterator
from types import ModuleType
from typing import BinaryIO, TextIO
from typing_extensions import TypeAlias

if sys.version_info >= (3, 9):
    from importlib.abc import Traversable

Package: TypeAlias = str | ModuleType
Resource: TypeAlias = str

def open_binary(package: Package, resource: Resource) -> BinaryIO: ...
def open_text(package: Package, resource: Resource, encoding: str = "utf-8", errors: str = "strict") -> TextIO: ...
def read_binary(package: Package, resource: Resource) -> bytes: ...
def read_text(package: Package, resource: Resource, encoding: str = "utf-8", errors: str = "strict") -> str: ...
def is_resource(package: Package, name: str) -> bool: ...
def contents(package: Package) -> Iterator[str]: ...

if sys.version_info >= (3, 12):
    def files(anchor: Package | None = ...) -> Traversable: ...

elif sys.version_info >= (3, 9):
    def files(package: Package) -> Traversable: ...

if sys.version_info >= (3, 10):
    from importlib.abc import ResourceReader as ResourceReader
