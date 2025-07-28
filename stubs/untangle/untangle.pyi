"""
untangle

Converts xml to python objects.

The only method you need to call is parse()

Partially inspired by xml2obj
(http://code.activestate.com/recipes/149368-xml2obj/)

Author: Christian Stefanescu (http://0chris.com)
License: MIT License - http://www.opensource.org/licenses/mit-license.php
"""

from collections.abc import Iterator, Mapping
from typing import Any
from typing_extensions import Self
from xml.sax import handler, xmlreader

def is_string(x: object) -> bool: ...

class Element:
    """
    Representation of an XML element.
    """

    children: list[Element]
    is_root: bool
    cdata: str
    def __init__(self, name: str | None, attributes: Mapping[str, Any] | None) -> None: ...
    def add_child(self, element: Element) -> None:
        """
        Store child elements.
        """

    def add_cdata(self, cdata: str) -> None:
        """
        Store cdata
        """

    def get_attribute(self, key: str) -> Any | None:
        """
        Get attributes by key
        """

    def get_elements(self, name: str | None = ...) -> list[Element]:
        """
        Find a child element by name
        """

    def __getitem__(self, key: str) -> Any | None: ...
    def __getattr__(self, key: str) -> Element: ...
    def __hasattribute__(self, name: str) -> bool: ...
    def __iter__(self) -> Iterator[Self]: ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    def __eq__(self, val: object) -> bool: ...
    def __dir__(self) -> list[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: str) -> bool: ...

class Handler(handler.ContentHandler):
    """
    SAX handler which creates the Python object structure out of ``Element``s
    """

    root: Element
    elements: list[Element]
    def __init__(self) -> None: ...
    def startElement(self, name: str, attributes: xmlreader.AttributesImpl) -> None: ...
    def endElement(self, name: str) -> None: ...
    def characters(self, cdata: str) -> None: ...

def parse(filename: str, **parser_features: bool) -> Element:
    """
    Interprets the given string as a filename, URL or XML data string,
    parses it and returns a Python object which represents the given
    document.

    Extra arguments to this function are treated as feature values that are
    passed to ``parser.setFeature()``. For example, ``feature_external_ges=False``
    will set ``xml.sax.handler.feature_external_ges`` to False, disabling
    the parser's inclusion of external general (text) entities such as DTDs.

    Raises ``ValueError`` if the first argument is None / empty string.

    Raises ``AttributeError`` if a requested xml.sax feature is not found in
    ``xml.sax.handler``.

    Raises ``xml.sax.SAXParseException`` if something goes wrong
    during parsing.

    Raises ``defusedxml.common.EntitiesForbidden``
    or ``defusedxml.common.ExternalReferenceForbidden``
    when a potentially malicious entity load is attempted. See also
    https://github.com/tiran/defusedxml#attack-vectors
    """

def is_url(string: str) -> bool:
    """
    Checks if the given string starts with 'http(s)'.
    """
