from _typeshed import StrPath
from typing import IO, AnyStr
from typing_extensions import Self

__tracebackhide__: bool

def contents_of[AnyStr: (bytes, str)](file: IO[AnyStr] | StrPath, encoding: str = "utf-8") -> str: ...

class FileMixin:
    def exists(self) -> Self: ...
    def does_not_exist(self) -> Self: ...
    def is_file(self) -> Self: ...
    def is_directory(self) -> Self: ...
    def is_named(self, filename: str) -> Self: ...
    def is_child_of(self, parent: str) -> Self: ...
