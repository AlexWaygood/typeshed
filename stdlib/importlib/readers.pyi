import importlib.resources.abc as abc
import zipfile
from _typeshed import Incomplete, StrPath
from collections.abc import Iterator
from io import BufferedReader
from typing import NoReturn
from typing_extensions import Literal, Never

class FileReader(abc.TraversableResources):
    def __init__(self, loader) -> None: ...
    def resource_path(self, resource: StrPath) -> str: ...
    def files(self) -> abc.Traversable: ...

class ZipReader(abc.TraversableResources):
    prefix: str
    archive: Incomplete
    def __init__(self, loader, module: str) -> None: ...
    def open_resource(self, resource: str) -> BufferedReader: ...
    def is_resource(self, path: StrPath) -> bool: ...
    def files(self) -> zipfile.Path: ...

class MultiplexedPath(abc.Traversable):
    def __init__(self, *paths: abc.Traversable) -> None: ...
    def iterdir(self) -> Iterator[abc.Traversable]: ...
    def read_bytes(self) -> NoReturn: ...
    def read_text(self, *args: Never, **kwargs: Never) -> NoReturn: ...  # type: ignore[override]
    def is_dir(self) -> Literal[True]: ...
    def is_file(self) -> Literal[False]: ...
    def joinpath(self, *descendants: str) -> abc.Traversable: ...
    def open(self, *args: Never, **kwargs: Never) -> NoReturn: ...  # type: ignore[override]
    @property
    def name(self) -> str: ...

class NamespaceReader(abc.TraversableResources):
    path: MultiplexedPath
    def __init__(self, namespace_path) -> None: ...
    def resource_path(self, resource: str) -> str: ...
    def files(self) -> MultiplexedPath: ...
