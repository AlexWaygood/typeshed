"""
Classes & functions that represent core elements of the PDF syntax

Most of what happens in a PDF happens in objects, which are formatted like so:
```
3 0 obj
<</Type /Page
/Parent 1 0 R
/Resources 2 0 R
/Contents 4 0 R>>
endobj
```

The first line says that this is the third object in the structure of the document.

There are 8 kinds of objects (Adobe Reference, 51):

* Boolean values
* Integer and real numbers
* Strings
* Names
* Arrays
* Dictionaries
* Streams
* The null object

The `<<` in the second line and the `>>` in the line preceding `endobj` denote
that it is a dictionary object. Dictionaries map Names to other objects.

Names are the strings preceded by `/`, valid Names do not have to start with a
capital letter, they can be any ascii characters, # and two characters can
escape non-printable ascii characters, described on page 57.

`3 0 obj` means what follows here is the third object, but the name Type
(represented here by `/Type`) is mapped to an indirect object reference:
`0 obj` vs `0 R`.

The structure of this data, in python/dict form, is thus:
```
third_obj = {
  '/Type': '/Page'),
  '/Parent': iobj_ref(1),
  '/Resources': iobj_ref(2),
  '/Contents': iobj_ref(4),
}
```

Content streams are of the form:
```
4 0 obj
<</Filter /ASCIIHexDecode /Length 22>>
stream
68656c6c6f20776f726c64
endstream
endobj
```

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

import datetime
from _typeshed import Incomplete, SupportsItems
from abc import ABC, abstractmethod
from re import Pattern
from typing import ClassVar, Literal, TypeVar
from typing_extensions import Self

from .encryption import StandardSecurityHandler

_T = TypeVar("_T")

def clear_empty_fields(d): ...
def create_dictionary_string(
    dict_,
    open_dict: str = "<<",
    close_dict: str = ">>",
    field_join: str = "\n",
    key_value_join: str = " ",
    has_empty_fields: bool = False,
) -> str:
    """format dictionary as PDF dictionary

    @param dict_: dictionary of values to render
    @param open_dict: string to open PDF dictionary
    @param close_dict: string to close PDF dictionary
    @param field_join: string to join fields with
    @param key_value_join: string to join key to value with
    @param has_empty_fields: whether or not to clear_empty_fields first.
    """

def create_list_string(list_):
    """format list of strings as PDF array"""

def iobj_ref(n):
    """format an indirect PDF Object reference from its id number"""

def create_stream(stream: str | bytes | bytearray, encryption_handler: StandardSecurityHandler | None = None, obj_id=None): ...

class Raw(str):
    """str subclass signifying raw data to be directly emitted to PDF without transformation."""

class Name(str):
    """str subclass signifying a PDF name, which are emitted differently than normal strings."""

    NAME_ESC: ClassVar[Pattern[bytes]]
    def serialize(self) -> str: ...

class PDFObject:
    @property
    def id(self) -> int: ...
    @id.setter
    def id(self, n: int) -> None: ...
    @property
    def ref(self) -> str: ...
    def serialize(self, obj_dict=None, _security_handler: StandardSecurityHandler | None = None) -> str:
        """Serialize the PDF object as an obj<</>>endobj text block"""

    def content_stream(self) -> bytes:
        """Subclasses can override this method to indicate the presence of a content stream"""

class PDFContentStream(PDFObject):
    filter: Name | None
    length: int
    def __init__(self, contents: bytes, compress: bool = False) -> None: ...

def build_obj_dict(key_values: SupportsItems[str, Incomplete]) -> dict[str, str]:
    """
    Build the PDF Object associative map to serialize, based on a key-values dict.
    The property names are converted from snake_case to CamelCase,
    and prefixed with a slash character "/".
    """

def camel_case(snake_case: str) -> str: ...

class PDFString(str):
    USE_HEX_ENCODING: ClassVar[bool]
    encrypt: bool
    def __new__(cls, content: str, encrypt: bool = False) -> Self:
        """
        Args:
            content (str): text
            encrypt (bool): if document encryption is enabled, should this string be encrypted?
        """

    def serialize(self) -> str: ...

class PDFDate:
    date: datetime.datetime
    with_tz: bool
    encrypt: bool

    def __init__(self, date: datetime.datetime, with_tz: bool = False, encrypt: bool = False) -> None:
        """
        Args:
            date (datetime): self-explanatory
            with_tz (bool): should the timezone be encoded in included in the date?
            encrypt (bool): if document encryption is enabled, should this string be encrypted?
        """

    def serialize(self) -> str: ...

class PDFArray(list[_T]):
    def serialize(self) -> str: ...

class Destination(ABC):
    @abstractmethod
    def serialize(self) -> str: ...

class DestinationXYZ(Destination):
    page_number: int
    top: float
    left: float
    zoom: float | Literal["null"]
    page_ref: Incomplete | None
    def __init__(self, page: int, top: float, left: float = 0, zoom: float | Literal["null"] = "null") -> None: ...
    def serialize(self) -> str: ...
    def replace(
        self, page=None, top: float | None = None, left: float | None = None, zoom: float | Literal["null"] | None = None
    ) -> DestinationXYZ: ...
