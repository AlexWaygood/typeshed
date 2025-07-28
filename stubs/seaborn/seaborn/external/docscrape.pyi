"""Extract reference documentation from the NumPy source tree.

Copyright (C) 2008 Stefan van der Walt <stefan@mentat.za.net>, Pauli Virtanen <pav@iki.fi>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

"""

from _typeshed import Incomplete, Unused
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableSequence
from typing import Any, ClassVar, NamedTuple, SupportsIndex, TypeVar, overload

_S = TypeVar("_S", bound=MutableSequence[str])

def strip_blank_lines(l: _S) -> _S:
    """Remove leading and trailing blank lines from a list of lines"""

class Reader:
    """A line-based string reader."""

    def __init__(self, data: str | list[str]) -> None:
        """
                Parameters
                ----------
                data : str
                   String with lines separated by '
        '.

        """

    @overload
    def __getitem__(self, n: slice) -> list[str]: ...
    @overload
    def __getitem__(self, n: SupportsIndex) -> str: ...
    def reset(self) -> None: ...
    def read(self) -> str: ...
    def seek_next_non_empty_line(self) -> None: ...
    def eof(self) -> bool: ...
    def read_to_condition(self, condition_func: Callable[[str], bool]) -> list[str]: ...
    def read_to_next_empty_line(self) -> list[str]: ...
    def read_to_next_unindented_line(self) -> list[str]: ...
    def peek(self, n: int = 0) -> str: ...
    def is_empty(self) -> bool: ...

class ParseError(Exception): ...

class Parameter(NamedTuple):
    """Parameter(name, type, desc)"""

    name: str
    type: str
    desc: list[str]

class NumpyDocString(Mapping[str, Any]):
    """Parses a numpydoc string to an abstract representation

    Instances define a mapping from section title to structured data.

    """

    sections: ClassVar[dict[str, Any]]
    def __init__(self, docstring: str, config: Unused = {}) -> None: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, val: Any) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    empty_description: str

def indent(str: str | None, indent: int = 4) -> str: ...
def dedent_lines(lines: Iterable[str]) -> list[str]:
    """Deindent a list of lines maximally"""

def header(text: str, style: str = "-") -> str: ...

class FunctionDoc(NumpyDocString):
    def __init__(self, func: object, role: str = "func", doc: str | None = None, config: Unused = {}) -> None: ...
    def get_func(self) -> tuple[Incomplete, str]: ...

class ClassDoc(NumpyDocString):
    extra_public_methods: list[str]
    show_inherited_members: bool
    @overload
    def __init__(
        self, cls: None, doc: str, modulename: str = "", func_doc: type[FunctionDoc] = ..., config: Mapping[str, Any] = {}
    ) -> None: ...
    @overload
    def __init__(
        self,
        cls: type,
        doc: str | None = None,
        modulename: str = "",
        func_doc: type[FunctionDoc] = ...,
        config: Mapping[str, Any] = {},
    ) -> None: ...
    @property
    def methods(self) -> list[str]: ...
    @property
    def properties(self) -> list[str]: ...
