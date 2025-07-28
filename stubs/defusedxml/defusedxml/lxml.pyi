"""DEPRECATED Example code for lxml.etree protection

The code has NO protection against decompression bombs.
"""

import threading
from _typeshed import Incomplete
from typing import Final, Literal

# Not bothering with types here as lxml support is supposed to be dropped in a future version of defusedxml

LXML3: bool
__origin__: Final = "lxml.etree"

def tostring(
    element_or_tree,
    *,
    encoding: str | None = None,
    method: Literal["xml", "html", "text", "c14n", "c14n2"] = "xml",
    xml_declaration: bool | None = None,
    pretty_print: bool = False,
    with_tail: bool = True,
    standalone: bool | None = None,
    doctype=None,
    exclusive: bool = False,
    inclusive_ns_prefixes=None,
    with_comments: bool = True,
    strip_text: bool = False,
):
    """tostring(element_or_tree, encoding=None, method="xml",
                 xml_declaration=None, pretty_print=False, with_tail=True,
                 standalone=None, doctype=None,
                 exclusive=False, inclusive_ns_prefixes=None,
                 with_comments=True, strip_text=False,
                 )

    Serialize an element to an encoded string representation of its XML
    tree.

    Defaults to ASCII encoding without XML declaration.  This
    behaviour can be configured with the keyword arguments 'encoding'
    (string) and 'xml_declaration' (bool).  Note that changing the
    encoding to a non UTF-8 compatible encoding will enable a
    declaration by default.

    You can also serialise to a Unicode string without declaration by
    passing the name ``'unicode'`` as encoding (or the ``str`` function
    in Py3 or ``unicode`` in Py2).  This changes the return value from
    a byte string to an unencoded unicode string.

    The keyword argument 'pretty_print' (bool) enables formatted XML.

    The keyword argument 'method' selects the output method: 'xml',
    'html', plain 'text' (text content without tags), 'c14n' or 'c14n2'.
    Default is 'xml'.

    With ``method="c14n"`` (C14N version 1), the options ``exclusive``,
    ``with_comments`` and ``inclusive_ns_prefixes`` request exclusive
    C14N, include comments, and list the inclusive prefixes respectively.

    With ``method="c14n2"`` (C14N version 2), the ``with_comments`` and
    ``strip_text`` options control the output of comments and text space
    according to C14N 2.0.

    Passing a boolean value to the ``standalone`` option will output
    an XML declaration with the corresponding ``standalone`` flag.

    The ``doctype`` option allows passing in a plain string that will
    be serialised before the XML tree.  Note that passing in non
    well-formed content here will make the XML output non well-formed.
    Also, an existing doctype in the document tree will not be removed
    when serialising an ElementTree instance.

    You can prevent the tail text of the element from being serialised
    by passing the boolean ``with_tail`` option.  This has no impact
    on the tail text of children, which will always be serialised.
    """

# Should be imported from lxml.etree.ElementBase, but lxml lacks types
class _ElementBase: ...

class RestrictedElement(_ElementBase):
    """A restricted Element class that filters out instances of some classes"""

    blacklist: Incomplete
    def __iter__(self): ...
    def iterchildren(self, tag: Incomplete | None = ..., reversed: bool = ...): ...
    def iter(self, tag: Incomplete | None = ..., *tags): ...
    def iterdescendants(self, tag: Incomplete | None = ..., *tags): ...
    def itersiblings(self, tag: Incomplete | None = ..., preceding: bool = ...): ...
    def getchildren(self): ...
    def getiterator(self, tag: Incomplete | None = ...): ...

class GlobalParserTLS(threading.local):
    """Thread local context for custom parser instances"""

    parser_config: Incomplete
    element_class: Incomplete
    def createDefaultParser(self): ...
    def setDefaultParser(self, parser) -> None: ...
    def getDefaultParser(self): ...

def getDefaultParser(): ...
def check_docinfo(elementtree, forbid_dtd: bool = False, forbid_entities: bool = True) -> None:
    """Check docinfo of an element tree for DTD and entity declarations

    The check for entity declarations needs lxml 3 or newer. lxml 2.x does
    not support dtd.iterentities().
    """

def parse(
    source,
    parser: Incomplete | None = ...,
    base_url: Incomplete | None = ...,
    forbid_dtd: bool = ...,
    forbid_entities: bool = ...,
): ...
def fromstring(
    text, parser: Incomplete | None = ..., base_url: Incomplete | None = ..., forbid_dtd: bool = ..., forbid_entities: bool = ...
): ...

XML = fromstring

def iterparse(*args, **kwargs) -> None: ...
