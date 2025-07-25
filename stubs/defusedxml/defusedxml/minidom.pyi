"""Defused xml.dom.minidom"""

from _typeshed import SupportsRead
from typing import Final
from xml.dom.minidom import Document
from xml.sax.xmlreader import XMLReader

__origin__: Final = "xml.dom.minidom"

def parse(
    file: str | SupportsRead[bytes | str],
    parser: XMLReader | None = None,
    bufsize: int | None = None,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Document:
    """Parse a file into a DOM by filename or file object."""

def parseString(
    string: str,
    parser: XMLReader | None = None,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Document:
    """Parse a file into a DOM from a string."""
