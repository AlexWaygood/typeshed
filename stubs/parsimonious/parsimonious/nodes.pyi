"""Nodes that make up parse trees

Parsing spits out a tree of these, which you can then tell to walk itself and
spit out a useful value. Or you can walk it yourself; the structural attributes
are public.

"""

from _typeshed import Incomplete
from collections.abc import Callable, Iterator, Sequence
from re import Match
from typing import Any, Generic, TypeVar

from parsimonious.exceptions import VisitationError as VisitationError
from parsimonious.expressions import Expression
from parsimonious.grammar import Grammar

class Node:
    """A parse tree node

    Consider these immutable once constructed. As a side effect of a
    memory-saving strategy in the cache, multiple references to a single
    ``Node`` might be returned in a single parse tree. So, if you start
    messing with one, you'll see surprising parallel changes pop up elsewhere.

    My philosophy is that parse trees (and their nodes) should be
    representation-agnostic. That is, they shouldn't get all mixed up with what
    the final rendered form of a wiki page (or the intermediate representation
    of a programming language, or whatever) is going to be: you should be able
    to parse once and render several representations from the tree, one after
    another.

    """

    expr: Expression
    full_text: str
    start: int
    end: int
    children: Sequence[Node]
    def __init__(
        self, expr: Expression, full_text: str, start: int, end: int, children: Sequence[Node] | None = None
    ) -> None: ...
    @property
    def expr_name(self) -> str: ...
    def __iter__(self) -> Iterator[Node]:
        """Support looping over my children and doing tuple unpacks on me.

        It can be very handy to unpack nodes in arg lists; see
        :class:`PegVisitor` for an example.

        """

    @property
    def text(self) -> str:
        """Return the text this node matched."""

    def prettily(self, error: Node | None = None) -> str:
        """Return a unicode, pretty-printed representation of me.

        :arg error: The node to highlight because an error occurred there

        """

    def __repr__(self, top_level: bool = True) -> str:
        """Return a bit of code (though not an expression) that will recreate
        me.
        """

class RegexNode(Node):
    """Node returned from a ``Regex`` expression

    Grants access to the ``re.Match`` object, in case you want to access
    capturing groups, etc.

    """

    match: Match[str]

class RuleDecoratorMeta(type): ...

_VisitResultT = TypeVar("_VisitResultT")
_ChildT = TypeVar("_ChildT")

class NodeVisitor(Generic[_VisitResultT], metaclass=RuleDecoratorMeta):
    """A shell for writing things that turn parse trees into something useful

    Performs a depth-first traversal of an AST. Subclass this, add methods for
    each expr you care about, instantiate, and call
    ``visit(top_node_of_parse_tree)``. It'll return the useful stuff. This API
    is very similar to that of ``ast.NodeVisitor``.

    These could easily all be static methods, but that would add at least as
    much weirdness at the call site as the ``()`` for instantiation. And this
    way, we support subclasses that require state: options, for example, or a
    symbol table constructed from a programming language's AST.

    We never transform the parse tree in place, because...

    * There are likely multiple references to the same ``Node`` object in a
      parse tree, and changes to one reference would surprise you elsewhere.
    * It makes it impossible to report errors: you'd end up with the "error"
      arrow pointing someplace in a half-transformed mishmash of nodes--and
      that's assuming you're even transforming the tree into another tree.
      Heaven forbid you're making it into a string or something else.

    """

    grammar: Grammar | Incomplete
    unwrapped_exceptions: tuple[type[BaseException], ...]
    def visit(self, node: Node) -> _VisitResultT:
        """Walk a parse tree, transforming it into another representation.

        Recursively descend a parse tree, dispatching to the method named after
        the rule in the :class:`~parsimonious.grammar.Grammar` that produced
        each node. If, for example, a rule was... ::

            bold = '<b>'

        ...the ``visit_bold()`` method would be called. It is your
        responsibility to subclass :class:`NodeVisitor` and implement those
        methods.

        """

    def generic_visit(self, node: Node, visited_children: Sequence[Any]):
        """Default visitor method

        :arg node: The node we're visiting
        :arg visited_children: The results of visiting the children of that
            node, in a list

        I'm not sure there's an implementation of this that makes sense across
        all (or even most) use cases, so we leave it to subclasses to implement
        for now.

        """

    def parse(self, text: str, pos: int = 0) -> _VisitResultT:
        """Parse some text with this Visitor's default grammar and return the
        result of visiting it.

        ``SomeVisitor().parse('some_string')`` is a shortcut for
        ``SomeVisitor().visit(some_grammar.parse('some_string'))``.

        """

    def match(self, text: str, pos: int = 0) -> _VisitResultT:
        """Parse and visit some text with this Visitor's default grammar, but
        don't insist on parsing all the way to the end.

        ``SomeVisitor().match('some_string')`` is a shortcut for
        ``SomeVisitor().visit(some_grammar.match('some_string'))``.

        """

    def lift_child(self, node: Node, children: Sequence[_ChildT]) -> _ChildT:
        """Lift the sole child of ``node`` up to replace the node."""

_CallableT = TypeVar("_CallableT", bound=Callable[..., Any])

def rule(rule_string: str) -> Callable[[_CallableT], _CallableT]:
    """Decorate a NodeVisitor ``visit_*`` method to tie a grammar rule to it.

    The following will arrange for the ``visit_digit`` method to receive the
    results of the ``~"[0-9]"`` parse rule::

        @rule('~"[0-9]"')
        def visit_digit(self, node, visited_children):
            ...

    Notice that there is no "digit = " as part of the rule; that gets inferred
    from the method name.

    In cases where there is only one kind of visitor interested in a grammar,
    using ``@rule`` saves you having to look back and forth between the visitor
    and the grammar definition.

    On an implementation level, all ``@rule`` rules get stitched together into
    a :class:`~parsimonious.Grammar` that becomes the NodeVisitor's
    :term:`default grammar`.

    Typically, the choice of a default rule for this grammar is simple: whatever
    ``@rule`` comes first in the class is the default. But the choice may become
    surprising if you divide the ``@rule`` calls among subclasses. At the
    moment, which method "comes first" is decided simply by comparing line
    numbers, so whatever method is on the smallest-numbered line will be the
    default. In a future release, this will change to pick the
    first ``@rule`` call on the basemost class that has one. That way, a
    subclass which does not override the default rule's ``visit_*`` method
    won't unintentionally change which rule is the default.

    """
