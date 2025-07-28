"""A convenience which constructs expression trees from an easy-to-read syntax

Use this unless you have a compelling reason not to; it performs some
optimizations that would be tedious to do when constructing an expression tree
by hand.

"""

import collections.abc
from _typeshed import Incomplete
from collections import OrderedDict
from collections.abc import Callable, Mapping
from typing import Any, NoReturn

from parsimonious.expressions import _CALLABLE_TYPE, Expression, Literal, Lookahead, OneOf, Regex, Sequence, TokenMatcher
from parsimonious.nodes import Node, NodeVisitor

class Grammar(OrderedDict[str, Expression]):
    """A collection of rules that describe a language

    You can start parsing from the default rule by calling ``parse()``
    directly on the ``Grammar`` object::

        g = Grammar('''
                    polite_greeting = greeting ", my good " title
                    greeting        = "Hi" / "Hello"
                    title           = "madam" / "sir"
                    ''')
        g.parse('Hello, my good sir')

    Or start parsing from any of the other rules; you can pull them out of the
    grammar as if it were a dictionary::

        g['title'].parse('sir')

    You could also just construct a bunch of ``Expression`` objects yourself
    and stitch them together into a language, but using a ``Grammar`` has some
    important advantages:

    * Languages are much easier to define in the nice syntax it provides.
    * Circular references aren't a pain.
    * It does all kinds of whizzy space- and time-saving optimizations, like
      factoring up repeated subexpressions into a single object, which should
      increase cache hit ratio. [Is this implemented yet?]

    """

    default_rule: Expression | Incomplete
    def __init__(self, rules: str = "", **more_rules: Expression | _CALLABLE_TYPE) -> None:
        """Construct a grammar.

        :arg rules: A string of production rules, one per line.
        :arg default_rule: The name of the rule invoked when you call
            :meth:`parse()` or :meth:`match()` on the grammar. Defaults to the
            first rule. Falls back to None if there are no string-based rules
            in this grammar.
        :arg more_rules: Additional kwargs whose names are rule names and
            values are Expressions or custom-coded callables which accomplish
            things the built-in rule syntax cannot. These take precedence over
            ``rules`` in case of naming conflicts.

        """

    def default(self, rule_name: str) -> Grammar:
        """Return a new Grammar whose :term:`default rule` is ``rule_name``."""

    def parse(self, text: str, pos: int = 0) -> Node:
        """Parse some text with the :term:`default rule`.

        :arg pos: The index at which to start parsing

        """

    def match(self, text: str, pos: int = 0) -> Node:
        """Parse some text with the :term:`default rule` but not necessarily
        all the way to the end.

        :arg pos: The index at which to start parsing

        """

class TokenGrammar(Grammar):
    """A Grammar which takes a list of pre-lexed tokens instead of text

    This is useful if you want to do the lexing yourself, as a separate pass:
    for example, to implement indentation-based languages.

    """

class BootstrappingGrammar(Grammar):
    """The grammar used to recognize the textual rules that describe other
    grammars

    This grammar gets its start from some hard-coded Expressions and claws its
    way from there to an expression tree that describes how to parse the
    grammar description syntax.

    """

rule_syntax: str

class LazyReference(str):
    """A lazy reference to a rule, which we resolve after grokking all the
    rules
    """

    name: str
    def resolve_refs(self, rule_map: Mapping[str, Expression | LazyReference]) -> Expression:
        """
        Traverse the rule map following top-level lazy references,
        until we reach a cycle (raise an error) or a concrete expression.

        For example, the following is a circular reference:
            foo = bar
            baz = foo2
            foo2 = foo

        Note that every RHS of a grammar rule _must_ be either a
        LazyReference or a concrete expression, so the reference chain will
        eventually either terminate or find a cycle.
        """

class RuleVisitor(NodeVisitor[tuple[OrderedDict[str, Expression], Expression | None]]):
    """Turns a parse tree of a grammar definition into a map of ``Expression``
    objects

    This is the magic piece that breathes life into a parsed bunch of parse
    rules, allowing them to go forth and parse other things.

    """

    quantifier_classes: dict[str, type[Expression]]
    visit_expression: Callable[[RuleVisitor, Node, collections.abc.Sequence[Any]], Any]
    visit_term: Callable[[RuleVisitor, Node, collections.abc.Sequence[Any]], Any]
    visit_atom: Callable[[RuleVisitor, Node, collections.abc.Sequence[Any]], Any]
    custom_rules: dict[str, Expression]
    def __init__(self, custom_rules: Mapping[str, Expression] | None = None) -> None:
        """Construct.

        :arg custom_rules: A dict of {rule name: expression} holding custom
            rules which will take precedence over the others

        """

    def visit_parenthesized(self, node: Node, parenthesized: collections.abc.Sequence[Any]) -> Expression:
        """Treat a parenthesized subexpression as just its contents.

        Its position in the tree suffices to maintain its grouping semantics.

        """

    def visit_quantifier(self, node: Node, quantifier: collections.abc.Sequence[Any]) -> Node:
        """Turn a quantifier into just its symbol-matching node."""

    def visit_quantified(self, node: Node, quantified: collections.abc.Sequence[Any]) -> Expression: ...
    def visit_lookahead_term(self, node: Node, lookahead_term: collections.abc.Sequence[Any]) -> Lookahead: ...
    def visit_not_term(self, node: Node, not_term: collections.abc.Sequence[Any]) -> Lookahead: ...
    def visit_rule(self, node: Node, rule: collections.abc.Sequence[Any]) -> Expression:
        """Assign a name to the Expression and return it."""

    def visit_sequence(self, node: Node, sequence: collections.abc.Sequence[Any]) -> Sequence:
        """A parsed Sequence looks like [term node, OneOrMore node of
        ``another_term``s]. Flatten it out.
        """

    def visit_ored(self, node: Node, ored: collections.abc.Sequence[Any]) -> OneOf: ...
    def visit_or_term(self, node: Node, or_term: collections.abc.Sequence[Any]) -> Expression:
        """Return just the term from an ``or_term``.

        We already know it's going to be ored, from the containing ``ored``.

        """

    def visit_label(self, node: Node, label: collections.abc.Sequence[Any]) -> str:
        """Turn a label into a unicode string."""

    def visit_reference(self, node: Node, reference: collections.abc.Sequence[Any]) -> LazyReference:
        """Stick a :class:`LazyReference` in the tree as a placeholder.

        We resolve them all later.

        """

    def visit_regex(self, node: Node, regex: collections.abc.Sequence[Any]) -> Regex:
        """Return a ``Regex`` expression."""

    def visit_spaceless_literal(self, spaceless_literal: Node, visited_children: collections.abc.Sequence[Any]) -> Literal:
        """Turn a string literal into a ``Literal`` that recognizes it."""

    def visit_literal(self, node: Node, literal: collections.abc.Sequence[Any]) -> Literal:
        """Pick just the literal out of a literal-and-junk combo."""

    def generic_visit(self, node: Node, visited_children: collections.abc.Sequence[Any]) -> collections.abc.Sequence[Any] | Node:
        """Replace childbearing nodes with a list of their children; keep
        others untouched.

        For our case, if a node has children, only the children are important.
        Otherwise, keep the node around for (for example) the flags of the
        regex rule. Most of these kept-around nodes are subsequently thrown
        away by the other visitor methods.

        We can't simply hang the visited children off the original node; that
        would be disastrous if the node occurred in more than one place in the
        tree.

        """

    def visit_rules(
        self, node: Node, rules_list: collections.abc.Sequence[Any]
    ) -> tuple[OrderedDict[str, Expression], Expression | None]:
        """Collate all the rules into a map. Return (map, default rule).

        The default rule is the first one. Or, if you have more than one rule
        of that name, it's the last-occurring rule of that name. (This lets you
        override the default rule when you extend a grammar.) If there are no
        string-based rules, the default rule is None, because the custom rules,
        due to being kwarg-based, are unordered.

        """

class TokenRuleVisitor(RuleVisitor):
    """A visitor which builds expression trees meant to work on sequences of
    pre-lexed tokens rather than strings
    """

    def visit_spaceless_literal(self, spaceless_literal: Node, visited_children: collections.abc.Sequence[Any]) -> TokenMatcher:
        """Turn a string literal into a ``TokenMatcher`` that matches
        ``Token`` objects by their ``type`` attributes.
        """

    def visit_regex(self, node: Node, regex: collections.abc.Sequence[Any]) -> NoReturn: ...

rule_grammar: Grammar
