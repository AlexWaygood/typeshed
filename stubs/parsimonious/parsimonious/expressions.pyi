"""Subexpressions that make up a parsed grammar

These do the parsing.

"""

import collections.abc
from collections.abc import Callable, Mapping
from re import Pattern
from typing import Any
from typing_extensions import Self, TypeAlias

from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import Node
from parsimonious.utils import StrAndRepr

_CALLABLE_RETURN_TYPE: TypeAlias = int | tuple[int, list[Node]] | Node | None
_CALLABLE_TYPE: TypeAlias = (
    Callable[[str, int], _CALLABLE_RETURN_TYPE]
    | Callable[[str, int, Mapping[tuple[int, int], Node], ParseError, Grammar], _CALLABLE_RETURN_TYPE]
)

def is_callable(value: object) -> bool: ...
def expression(callable: _CALLABLE_TYPE, rule_name: str, grammar: Grammar) -> Expression:
    """Turn a plain callable into an Expression.

    The callable can be of this simple form::

        def foo(text, pos):
            '''If this custom expression matches starting at text[pos], return
            the index where it stops matching. Otherwise, return None.'''
            if the expression matched:
                return end_pos

    If there child nodes to return, return a tuple::

        return end_pos, children

    If the expression doesn't match at the given ``pos`` at all... ::

        return None

    If your callable needs to make sub-calls to other rules in the grammar or
    do error reporting, it can take this form, gaining additional arguments::

        def foo(text, pos, cache, error, grammar):
            # Call out to other rules:
            node = grammar['another_rule'].match_core(text, pos, cache, error)
            ...
            # Return values as above.

    The return value of the callable, if an int or a tuple, will be
    automatically transmuted into a :class:`~parsimonious.Node`. If it returns
    a Node-like class directly, it will be passed through unchanged.

    :arg rule_name: The rule name to attach to the resulting
        :class:`~parsimonious.Expression`
    :arg grammar: The :class:`~parsimonious.Grammar` this expression will be a
        part of, to make delegating to other rules possible

    """

IN_PROGRESS: object

class Expression(StrAndRepr):
    """A thing that can be matched against a piece of text"""

    name: str
    identity_tuple: tuple[str]
    def __init__(self, name: str = "") -> None: ...
    def resolve_refs(self, rule_map: Mapping[str, Expression]) -> Self: ...
    def parse(self, text: str, pos: int = 0) -> Node:
        """Return a parse tree of ``text``.

        Raise ``ParseError`` if the expression wasn't satisfied. Raise
        ``IncompleteParseError`` if the expression was satisfied but didn't
        consume the full string.

        """

    def match(self, text: str, pos: int = 0) -> Node:
        """Return the parse tree matching this expression at the given
        position, not necessarily extending all the way to the end of ``text``.

        Raise ``ParseError`` if there is no match there.

        :arg pos: The index at which to start matching

        """

    def match_core(self, text: str, pos: int, cache: Mapping[tuple[int, int], Node], error: ParseError) -> Node:
        """Internal guts of ``match()``

        This is appropriate to call only from custom rules or Expression
        subclasses.

        :arg cache: The packrat cache::

            {(oid, pos): Node tree matched by object `oid` at index `pos` ...}

        :arg error: A ParseError instance with ``text`` already filled in but
            otherwise blank. We update the error reporting info on this object
            as we go. (Sticking references on an existing instance is faster
            than allocating a new one for each expression that fails.) We
            return None rather than raising and catching ParseErrors because
            catching is slow.

        """

    def as_rule(self) -> str:
        """Return the left- and right-hand sides of a rule that represents me.

        Return unicode. If I have no ``name``, omit the left-hand side.

        """

class Literal(Expression):
    """A string literal

    Use these if you can; they're the fastest.

    """

    literal: str
    identity_tuple: tuple[str, str]  # type: ignore[assignment]
    def __init__(self, literal: str, name: str = "") -> None: ...

class TokenMatcher(Literal):
    """An expression matching a single token of a given type

    This is for use only with TokenGrammars.

    """

class Regex(Expression):
    """An expression that matches what a regex does.

    Use these as much as you can and jam as much into each one as you can;
    they're fast.

    """

    re: Pattern[str]
    identity_tuple: tuple[str, Pattern[str]]  # type: ignore[assignment]
    def __init__(
        self,
        pattern: str,
        name: str = "",
        ignore_case: bool = False,
        locale: bool = False,
        multiline: bool = False,
        dot_all: bool = False,
        unicode: bool = False,
        verbose: bool = False,
        ascii: bool = False,
    ) -> None: ...

class Compound(Expression):
    """An abstract expression which contains other expressions"""

    members: collections.abc.Sequence[Expression]
    def __init__(self, *members: Expression, **kwargs: Any) -> None:
        """``members`` is a sequence of expressions."""

class Sequence(Compound):
    """A series of expressions that must match contiguous, ordered pieces of
    the text

    In other words, it's a concatenation operator: each piece has to match, one
    after another.

    """

class OneOf(Compound):
    """A series of expressions, one of which must match

    Expressions are tested in order from first to last. The first to succeed
    wins.

    """

class Lookahead(Compound):
    """An expression which consumes nothing, even if its contained expression
    succeeds
    """

    negativity: bool
    def __init__(self, member: Expression, *, negative: bool = False, **kwargs: Any) -> None: ...

def Not(term: Expression) -> Lookahead: ...

class Quantifier(Compound):
    """An expression wrapper like the */+/?/{n,m} quantifier in regexes."""

    min: int
    max: float
    def __init__(self, member: Expression, *, min: int = 0, max: float = ..., name: str = "", **kwargs: Any) -> None: ...

def ZeroOrMore(member: Expression, name: str = "") -> Quantifier: ...
def OneOrMore(member: Expression, name: str = "", min: int = 1) -> Quantifier: ...
def Optional(member: Expression, name: str = "") -> Quantifier: ...
