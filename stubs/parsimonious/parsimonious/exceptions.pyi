from parsimonious.expressions import Expression
from parsimonious.grammar import LazyReference
from parsimonious.nodes import Node
from parsimonious.utils import StrAndRepr

class ParseError(StrAndRepr, Exception):
    """A call to ``Expression.parse()`` or ``match()`` didn't match."""

    text: str
    pos: int
    expr: Expression | None
    def __init__(self, text: str, pos: int = -1, expr: Expression | None = None) -> None: ...
    def line(self) -> int:
        """Return the 1-based line number where the expression ceased to
        match.
        """

    def column(self) -> int:
        """Return the 1-based column where the expression ceased to match."""

class LeftRecursionError(ParseError): ...

class IncompleteParseError(ParseError):
    """A call to ``parse()`` matched a whole Expression but did not consume the
    entire text.
    """

class VisitationError(Exception):
    """Something went wrong while traversing a parse tree.

    This exception exists to augment an underlying exception with information
    about where in the parse tree the error occurred. Otherwise, it could be
    tiresome to figure out what went wrong; you'd have to play back the whole
    tree traversal in your head.

    """

    original_class: type[BaseException]
    def __init__(self, exc: BaseException, exc_class: type[BaseException], node: Node) -> None:
        """Construct.

        :arg exc: What went wrong. We wrap this and add more info.
        :arg node: The node at which the error occurred

        """

class BadGrammar(StrAndRepr, Exception):
    """Something was wrong with the definition of a grammar.

    Note that a ParseError might be raised instead if the error is in the
    grammar definition syntax.

    """

class UndefinedLabel(BadGrammar):
    """A rule referenced in a grammar was never defined.

    Circular references and forward references are okay, but you have to define
    stuff at some point.

    """

    label: LazyReference
    def __init__(self, label: LazyReference) -> None: ...
