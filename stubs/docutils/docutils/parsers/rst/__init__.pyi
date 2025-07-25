"""
This is ``docutils.parsers.rst`` package. It exports a single class, `Parser`,
the reStructuredText parser.


Usage
=====

1. Create a parser::

       parser = docutils.parsers.rst.Parser()

   Several optional arguments may be passed to modify the parser's behavior.
   Please see `Customizing the Parser`_ below for details.

2. Gather input (a multi-line string), by reading a file or the standard
   input::

       input = sys.stdin.read()

3. Create a new empty `docutils.nodes.document` tree::

       document = docutils.utils.new_document(source, settings)

   See `docutils.utils.new_document()` for parameter details.

4. Run the parser, populating the document tree::

       parser.parse(input, document)


Parser Overview
===============

The reStructuredText parser is implemented as a state machine, examining its
input one line at a time. To understand how the parser works, please first
become familiar with the `docutils.statemachine` module, then see the
`states` module.


Customizing the Parser
----------------------

Anything that isn't already customizable is that way simply because that type
of customizability hasn't been implemented yet.  Patches welcome!

When instantiating an object of the `Parser` class, two parameters may be
passed: ``rfc2822`` and ``inliner``.  Pass ``rfc2822=True`` to enable an
initial RFC-2822 style header block, parsed as a "field_list" element (with
"class" attribute set to "rfc2822").  Currently this is the only body-level
element which is customizable without subclassing.  (Tip: subclass `Parser`
and change its "state_classes" and "initial_state" attributes to refer to new
classes. Contact the author if you need more details.)

The ``inliner`` parameter takes an instance of `states.Inliner` or a subclass.
It handles inline markup recognition.  A common extension is the addition of
further implicit hyperlinks, like "RFC 2822".  This can be done by subclassing
`states.Inliner`, adding a new method for the implicit markup, and adding a
``(pattern, method)`` pair to the "implicit_dispatch" attribute of the
subclass.  See `states.Inliner.implicit_inline()` for details.  Explicit
inline markup can be customized in a `states.Inliner` subclass via the
``patterns.initial`` and ``dispatch`` attributes (and new methods as
appropriate).
"""

from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from typing import Any, ClassVar, Final, Literal
from typing_extensions import TypeAlias

from docutils import nodes, parsers
from docutils.parsers.rst.states import Inliner, RSTState, RSTStateMachine
from docutils.statemachine import StringList
from docutils.transforms import Transform
from docutils.utils import Reporter

__docformat__: Final = "reStructuredText"

class Parser(parsers.Parser):
    """The reStructuredText parser."""

    config_section_dependencies: ClassVar[tuple[str, ...]]
    initial_state: Literal["Body", "RFC2822Body"]
    state_classes: Sequence[type[RSTState]]
    inliner: Inliner | None
    statemachine: RSTStateMachine
    def __init__(self, rfc2822: bool = False, inliner: Inliner | None = None) -> None: ...
    def get_transforms(self) -> list[type[Transform]]: ...
    def parse(self, inputstring: str, document: nodes.document) -> None:
        """Parse `inputstring` and populate `document`, a document tree."""

class DirectiveError(Exception):
    """
    Store a message and a system message level.

    To be thrown from inside directive code.

    Do not instantiate directly -- use `Directive.directive_error()`
    instead!
    """

    level: int
    msg: str
    def __init__(self, level: int, message: str) -> None:
        """Set error `message` and `level`"""

class Directive:
    """
    Base class for reStructuredText directives.

    The following attributes may be set by subclasses.  They are
    interpreted by the directive parser (which runs the directive
    class):

    - `required_arguments`: The number of required arguments (default:
      0).

    - `optional_arguments`: The number of optional arguments (default:
      0).

    - `final_argument_whitespace`: A boolean, indicating if the final
      argument may contain whitespace (default: False).

    - `option_spec`: A dictionary, mapping known option names to
      conversion functions such as `int` or `float` (default: {}, no
      options).  Several conversion functions are defined in the
      directives/__init__.py module.

      Option conversion functions take a single parameter, the option
      argument (a string or ``None``), validate it and/or convert it
      to the appropriate form.  Conversion functions may raise
      `ValueError` and `TypeError` exceptions.

    - `has_content`: A boolean; True if content is allowed.  Client
      code must handle the case where content is required but not
      supplied (an empty content list will be supplied).

    Arguments are normally single whitespace-separated words.  The
    final argument may contain whitespace and/or newlines if
    `final_argument_whitespace` is True.

    If the form of the arguments is more complex, specify only one
    argument (either required or optional) and set
    `final_argument_whitespace` to True; the client code must do any
    context-sensitive parsing.

    When a directive implementation is being run, the directive class
    is instantiated, and the `run()` method is executed.  During
    instantiation, the following instance variables are set:

    - ``name`` is the directive type or name (string).

    - ``arguments`` is the list of positional arguments (strings).

    - ``options`` is a dictionary mapping option names (strings) to
      values (type depends on option conversion functions; see
      `option_spec` above).

    - ``content`` is a list of strings, the directive content line by line.

    - ``lineno`` is the absolute line number of the first line
      of the directive.

    - ``content_offset`` is the line offset of the first line
      of the content from the beginning of the current input.
      Used when initiating a nested parse.

    - ``block_text`` is a string containing the entire directive.

    - ``state`` is the state which called the directive function.

    - ``state_machine`` is the state machine which controls the state
      which called the directive function.

    - ``reporter`` is the state machine's `reporter` instance.

    Directive functions return a list of nodes which will be inserted
    into the document tree at the point where the directive was
    encountered.  This can be an empty list if there is nothing to
    insert.

    For ordinary directives, the list must contain body elements or
    structural elements.  Some directives are intended specifically
    for substitution definitions, and must return a list of `Text`
    nodes and/or inline elements (suitable for inline insertion, in
    place of the substitution reference).  Such directives must verify
    substitution definition context, typically using code like this::

        if not isinstance(state, states.SubstitutionDef):
            error = self.reporter.error(
                'Invalid context: the "%s" directive can only be used '
                'within a substitution definition.' % (name),
                nodes.literal_block(block_text, block_text), line=lineno)
            return [error]
    """

    required_arguments: ClassVar[int]
    optional_arguments: ClassVar[int]
    final_argument_whitespace: ClassVar[bool]
    option_spec: ClassVar[dict[str, Callable[[str], Incomplete]] | None]
    has_content: ClassVar[bool]
    name: str
    arguments: list[str]
    options: dict[str, Incomplete]
    content: StringList
    lineno: int
    content_offset: int
    block_text: str
    state: RSTState
    state_machine: RSTStateMachine = ...
    reporter: Reporter
    def __init__(
        self,
        name: str,
        arguments: list[str],
        options: dict[str, Incomplete],
        content: StringList,
        lineno: int,
        content_offset: int,
        block_text: str,
        state: RSTState,
        state_machine: RSTStateMachine,
    ) -> None: ...
    def run(self) -> Sequence[nodes.Node]: ...
    def directive_error(self, level: int, message: str) -> DirectiveError:
        """
        Return a DirectiveError suitable for being thrown as an exception.

        Call "raise self.directive_error(level, message)" from within
        a directive implementation to return one single system message
        at level `level`, which automatically gets the directive block
        and the line number added.

        Preferably use the `debug`, `info`, `warning`, `error`, or `severe`
        wrapper methods, e.g. ``self.error(message)`` to generate an
        ERROR-level directive error.
        """

    def debug(self, message: str) -> DirectiveError: ...
    def info(self, message: str) -> DirectiveError: ...
    def warning(self, message: str) -> DirectiveError: ...
    def error(self, message: str) -> DirectiveError: ...
    def severe(self, message: str) -> DirectiveError: ...
    def assert_has_content(self) -> None:
        """
        Throw an ERROR-level DirectiveError if the directive doesn't
        have contents.
        """

    def add_name(self, node: nodes.Node) -> None:
        """Append self.options['name'] to node['names'] if it exists.

        Also normalize the name string and register it as explicit target.
        """

_DirectiveFn: TypeAlias = Callable[
    [str, list[str], dict[str, Any], StringList, int, int, str, RSTState, RSTStateMachine], Directive
]

def convert_directive_function(directive_fn: _DirectiveFn) -> type[Directive]:
    """
    Define & return a directive class generated from `directive_fn`.

    `directive_fn` uses the old-style, functional interface.
    """
