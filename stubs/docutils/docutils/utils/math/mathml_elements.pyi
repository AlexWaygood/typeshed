"""MathML element classes based on `xml.etree`.

The module is intended for programmatic generation of MathML
and covers the part of `MathML Core`_ that is required by
Docutil's *TeX math to MathML* converter.

This module is PROVISIONAL:
the API is not settled and may change with any minor Docutils version.

.. _MathML Core: https://www.w3.org/TR/mathml-core/
"""

import numbers
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from typing import ClassVar, Final, SupportsIndex, overload
from typing_extensions import Self

GLOBAL_ATTRIBUTES: Final[tuple[str, ...]]

class MathElement(ET.Element):
    """Base class for MathML elements."""

    nchildren: ClassVar[int | None]
    parent: MathElement | None
    def __init__(self, *children, **attributes: object) -> None:  # attributes is passed to self.a_str method
        """Set up node with `children` and `attributes`.

        Attribute names are normalised to lowercase.
        You may use "CLASS" to set a "class" attribute.
        Attribute values are converted to strings
        (with True -> "true" and False -> "false").

        >>> math(CLASS='test', level=3, split=True)
        math(class='test', level='3', split='true')
        >>> math(CLASS='test', level=3, split=True).toxml()
        '<math class="test" level="3" split="true"></math>'

        """

    @staticmethod
    def a_str(v: object) -> str: ...
    def set(self, key: str, value: object) -> None: ...  # value is passed to self.a_str method
    @overload  # type: ignore[override]
    def __setitem__(self, key: SupportsIndex, value: MathElement) -> None: ...
    @overload  # type: ignore[override]
    def __setitem__(self, key: slice, value: Iterable[MathElement]) -> None: ...
    def is_full(self) -> bool:
        """Return boolean indicating whether children may be appended."""

    def close(self) -> MathElement | None:
        """Close element and return first non-full anchestor or None."""

    def append(self, element: MathElement) -> Self:  # type: ignore[override]
        """Append `element` and return new "current node" (insertion point).

        Append as child element and set the internal `parent` attribute.

        If self is already full, raise TypeError.

        If self is full after appending, call `self.close()`
        (returns first non-full anchestor or None) else return `self`.
        """

    def extend(self, elements: Iterable[MathElement]) -> Self:  # type: ignore[override]
        """Sequentially append `elements`. Return new "current node".

        Raise TypeError if overfull.
        """

    def pop(self, index: int = -1): ...
    def in_block(self) -> bool:
        """Return True, if `self` or an ancestor has ``display='block'``.

        Used to find out whether we are in inline vs. displayed maths.
        """

    def indent_xml(self, space: str = "  ", level: int = 0) -> None:
        """Format XML output with indents.

        Use with care:
          Formatting whitespace is permanently added to the
          `text` and `tail` attributes of `self` and anchestors!
        """

    def unindent_xml(self) -> None:
        """Strip whitespace at the end of `text` and `tail` attributes...

        to revert changes made by the `indent_xml()` method.
        Use with care, trailing whitespace from the original may be lost.
        """

    def toxml(self, encoding: str | None = None) -> str:
        """Return an XML representation of the element.

        By default, the return value is a `str` instance. With an explicit
        `encoding` argument, the result is a `bytes` instance in the
        specified encoding. The XML default encoding is UTF-8, any other
        encoding must be specified in an XML document header.

        Name and encoding handling match `xml.dom.minidom.Node.toxml()`
        while `etree.Element.tostring()` returns `bytes` by default.
        """

class MathRow(MathElement):
    """Base class for elements treating content as a single mrow."""

class MathSchema(MathElement):
    """Base class for schemata expecting 2 or more children.

    The special attribute `switch` indicates that the last two child
    elements are in reversed order and must be switched before XML-export.
    See `msub` for an example.
    """

    nchildren: ClassVar[int]
    switch: bool
    def __init__(self, *children, switch: bool = False, **kwargs) -> None: ...

class MathToken(MathElement):
    """Token Element: contains textual data instead of children.

    Expect text data on initialisation.
    """

    nchildren: ClassVar[int]
    text: str
    def __init__(self, text: str | numbers.Number, **attributes: object) -> None: ...

class math(MathRow):
    """Top-level MathML element, a single mathematical formula."""

class mtext(MathToken):
    """Arbitrary text with no notational meaning."""

class mi(MathToken):
    """Identifier, such as a function name, variable or symbolic constant."""

class mn(MathToken):
    """Numeric literal.

    >>> mn(3.41).toxml()
    '<mn>3.41</mn>'

    Normally a sequence of digits with a possible separator (a dot or a comma).
    (Values with comma must be specified as `str`.)
    """

class mo(MathToken):
    """Operator, Fence, Separator, or Accent.

    >>> mo('<').toxml()
    '<mo>&lt;</mo>'

    Besides operators in strict mathematical meaning, this element also
    includes "operators" like parentheses, separators like comma and
    semicolon, or "absolute value" bars.
    """

class mspace(MathElement):
    """Blank space, whose size is set by its attributes.

    Takes additional attributes `depth`, `height`, `width`.
    Takes no children and no text.

    See also `mphantom`.
    """

    nchildren: ClassVar[int]

class mrow(MathRow):
    """Generic element to group children as a horizontal row.

    Removed on closing if not required (see `mrow.close()`).
    """

    def transfer_attributes(self, other) -> None:
        """Transfer attributes from self to other.

        "List values" (class, style) are appended to existing values,
        other values replace existing values.
        """

class mfrac(MathSchema):
    """Fractions or fraction-like objects such as binomial coefficients."""

class msqrt(MathRow):
    """Square root. See also `mroot`."""

    nchildren: ClassVar[int]

class mroot(MathSchema):
    """Roots with an explicit index. See also `msqrt`."""

class mstyle(MathRow):
    """Style Change.

    In modern browsers, <mstyle> is equivalent to an <mrow> element.
    However, <mstyle> may still be relevant for compatibility with
    MathML implementations outside browsers.
    """

class merror(MathRow):
    """Display contents as error messages."""

class menclose(MathRow):
    """Renders content inside an enclosing notation...

    ... specified by the notation attribute.

    Non-standard but still required by Firefox for boxed expressions.
    """

    nchildren: ClassVar[int]

class mpadded(MathRow):
    """Adjust space around content."""

class mphantom(MathRow):
    """Placeholder: Rendered invisibly but dimensions are kept."""

    nchildren: ClassVar[int]

class msub(MathSchema):
    """Attach a subscript to an expression."""

class msup(MathSchema):
    """Attach a superscript to an expression."""

class msubsup(MathSchema):
    """Attach both a subscript and a superscript to an expression."""

    nchildren: ClassVar[int]

class munder(msub):
    """Attach an accent or a limit under an expression."""

class mover(msup):
    """Attach an accent or a limit over an expression."""

class munderover(msubsup):
    """Attach accents or limits both under and over an expression."""

class mtable(MathElement):
    """Table or matrix element."""

class mtr(MathRow):
    """Row in a table or a matrix."""

class mtd(MathRow):
    """Cell in a table or a matrix"""
