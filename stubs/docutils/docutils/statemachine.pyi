"""
A finite state machine specialized for regular-expression-based text filters,
this module defines the following classes:

- `StateMachine`, a state machine
- `State`, a state superclass
- `StateMachineWS`, a whitespace-sensitive version of `StateMachine`
- `StateWS`, a state superclass for use with `StateMachineWS`
- `SearchStateMachine`, uses `re.search()` instead of `re.match()`
- `SearchStateMachineWS`, uses `re.search()` instead of `re.match()`
- `ViewList`, extends standard Python lists.
- `StringList`, string-specific ViewList.

Exception classes:

- `StateMachineError`
- `UnknownStateError`
- `DuplicateStateError`
- `UnknownTransitionError`
- `DuplicateTransitionError`
- `TransitionPatternNotFound`
- `TransitionMethodNotFound`
- `UnexpectedIndentationError`
- `TransitionCorrection`: Raised to switch to another transition.
- `StateCorrection`: Raised to switch to another state & transition.

Functions:

- `string2lines()`: split a multi-line string into a list of one-line strings


How To Use This Module
======================
(See the individual classes, methods, and attributes for details.)

1. Import it: ``import statemachine`` or ``from statemachine import ...``.
   You will also need to ``import re``.

2. Derive a subclass of `State` (or `StateWS`) for each state in your state
   machine::

       class MyState(statemachine.State):

   Within the state's class definition:

   a) Include a pattern for each transition, in `State.patterns`::

          patterns = {'atransition': r'pattern', ...}

   b) Include a list of initial transitions to be set up automatically, in
      `State.initial_transitions`::

          initial_transitions = ['atransition', ...]

   c) Define a method for each transition, with the same name as the
      transition pattern::

          def atransition(self, match, context, next_state):
              # do something
              result = [...]  # a list
              return context, next_state, result
              # context, next_state may be altered

      Transition methods may raise an `EOFError` to cut processing short.

   d) You may wish to override the `State.bof()` and/or `State.eof()` implicit
      transition methods, which handle the beginning- and end-of-file.

   e) In order to handle nested processing, you may wish to override the
      attributes `State.nested_sm` and/or `State.nested_sm_kwargs`.

      If you are using `StateWS` as a base class, in order to handle nested
      indented blocks, you may wish to:

      - override the attributes `StateWS.indent_sm`,
        `StateWS.indent_sm_kwargs`, `StateWS.known_indent_sm`, and/or
        `StateWS.known_indent_sm_kwargs`;
      - override the `StateWS.blank()` method; and/or
      - override or extend the `StateWS.indent()`, `StateWS.known_indent()`,
        and/or `StateWS.firstknown_indent()` methods.

3. Create a state machine object::

       sm = StateMachine(state_classes=[MyState, ...],
                         initial_state='MyState')

4. Obtain the input text, which needs to be converted into a tab-free list of
   one-line strings. For example, to read text from a file called
   'inputfile'::

       with open('inputfile', encoding='utf-8') as fp:
           input_string = fp.read()
       input_lines = statemachine.string2lines(input_string)

5. Run the state machine on the input text and collect the results, a list::

       results = sm.run(input_lines)

6. Remove any lingering circular references::

       sm.unlink()
"""

import sys
from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from re import Match, Pattern
from typing import Any, ClassVar, Final, Generic, SupportsIndex, TypeVar, overload
from typing_extensions import Self, TypeAlias

_T = TypeVar("_T")
_Context = TypeVar("_Context")
_TransitionResult: TypeAlias = tuple[_Context, str | None, list[str]]
_TransitionMethod: TypeAlias = Callable[[Match[str], _Context, str], _TransitionResult[_Context]]
_Observer: TypeAlias = Callable[[StateMachine[_Context]], None]

__docformat__: Final = "reStructuredText"

class StateMachine(Generic[_Context]):
    """
    A finite state machine for text filters using regular expressions.

    The input is provided in the form of a list of one-line strings (no
    newlines). States are subclasses of the `State` class. Transitions consist
    of regular expression patterns and transition methods, and are defined in
    each state.

    The state machine is started with the `run()` method, which returns the
    results of processing in a list.
    """

    input_lines: StringList | None
    input_offset: int
    line: str | None
    line_offset: int
    debug: bool
    initial_state: str
    current_state: str
    states: dict[str, State[_Context]]
    observers: list[_Observer[_Context]]
    def __init__(self, state_classes: Iterable[type[State[_Context]]], initial_state: str, debug: bool = False) -> None:
        """
        Initialize a `StateMachine` object; add state objects.

        Parameters:

        - `state_classes`: a list of `State` (sub)classes.
        - `initial_state`: a string, the class name of the initial state.
        - `debug`: a boolean; produce verbose output if true (nonzero).
        """

    def unlink(self) -> None:
        """Remove circular references to objects no longer required."""

    def run(
        self,
        input_lines: Sequence[str] | StringList,
        input_offset: int = 0,
        context: _Context | None = None,
        input_source: str | None = None,
        initial_state: str | None = None,
    ) -> list[str]:
        """
        Run the state machine on `input_lines`. Return results (a list).

        Reset `self.line_offset` and `self.current_state`. Run the
        beginning-of-file transition. Input one line at a time and check for a
        matching transition. If a match is found, call the transition method
        and possibly change the state. Store the context returned by the
        transition method to be passed on to the next transition matched.
        Accumulate the results returned by the transition methods in a list.
        Run the end-of-file transition. Finally, return the accumulated
        results.

        Parameters:

        - `input_lines`: a list of strings without newlines, or `StringList`.
        - `input_offset`: the line offset of `input_lines` from the beginning
          of the file.
        - `context`: application-specific storage.
        - `input_source`: name or path of source of `input_lines`.
        - `initial_state`: name of initial state.
        """

    def get_state(self, next_state: str | None = None) -> State[_Context]:
        """
        Return current state object; set it first if `next_state` given.

        Parameter `next_state`: a string, the name of the next state.

        Exception: `UnknownStateError` raised if `next_state` unknown.
        """

    def next_line(self, n: int = 1) -> str:
        """Load `self.line` with the `n`'th next line and return it."""

    def is_next_line_blank(self) -> bool:
        """Return True if the next line is blank or non-existent."""

    def at_eof(self) -> bool:
        """Return 1 if the input is at or past end-of-file."""

    def at_bof(self) -> bool:
        """Return 1 if the input is at or before beginning-of-file."""

    def previous_line(self, n: int = 1) -> str | None:
        """Load `self.line` with the `n`'th previous line and return it."""

    def goto_line(self, line_offset: int) -> str | None:
        """Jump to absolute line offset `line_offset`, load and return it."""

    def get_source(self, line_offset: int) -> str:
        """Return source of line at absolute line offset `line_offset`."""

    def abs_line_offset(self) -> int:
        """Return line offset of current line, from beginning of file."""

    def abs_line_number(self) -> int:
        """Return line number of current line (counting from 1)."""

    def get_source_and_line(self, lineno: int | None = None) -> tuple[str, int] | tuple[None, None]:
        """Return (source, line) tuple for current or given line number.

        Looks up the source and line number in the `self.input_lines`
        StringList instance to count for included source files.

        If the optional argument `lineno` is given, convert it from an
        absolute line number to the corresponding (source, line) pair.
        """

    def insert_input(self, input_lines: list[str] | StringList, source: str) -> None: ...
    def get_text_block(self, flush_left: bool = False) -> StringList:
        """
        Return a contiguous block of text.

        If `flush_left` is true, raise `UnexpectedIndentationError` if an
        indented line is encountered before the text block ends (with a blank
        line).
        """

    def check_line(
        self, context: _Context, state: State[_Context], transitions: list[str] | None = None
    ) -> _TransitionResult[_Context]:
        """
        Examine one line of input for a transition match & execute its method.

        Parameters:

        - `context`: application-dependent storage.
        - `state`: a `State` object, the current state.
        - `transitions`: an optional ordered list of transition names to try,
          instead of ``state.transition_order``.

        Return the values returned by the transition method:

        - context: possibly modified from the parameter `context`;
        - next state name (`State` subclass name);
        - the result output of the transition, a list.

        When there is no match, ``state.no_match()`` is called and its return
        value is returned.
        """

    def add_state(self, state_class: type[State[_Context]]) -> None:
        """
        Initialize & add a `state_class` (`State` subclass) object.

        Exception: `DuplicateStateError` raised if `state_class` was already
        added.
        """

    def add_states(self, state_classes: Iterable[type[State[_Context]]]) -> None:
        """
        Add `state_classes` (a list of `State` subclasses).
        """

    def runtime_init(self) -> None:
        """
        Initialize `self.states`.
        """

    def error(self) -> None:
        """Report error details."""

    def attach_observer(self, observer: _Observer[_Context]) -> None:
        """
        The `observer` parameter is a function or bound method which takes two
        arguments, the source and offset of the current line.
        """

    def detach_observer(self, observer: _Observer[_Context]) -> None: ...
    def notify_observers(self) -> None: ...

class State(Generic[_Context]):
    """
    State superclass. Contains a list of transitions, and transition methods.

    Transition methods all have the same signature. They take 3 parameters:

    - An `re` match object. ``match.string`` contains the matched input line,
      ``match.start()`` gives the start index of the match, and
      ``match.end()`` gives the end index.
    - A context object, whose meaning is application-defined (initial value
      ``None``). It can be used to store any information required by the state
      machine, and the returned context is passed on to the next transition
      method unchanged.
    - The name of the next state, a string, taken from the transitions list;
      normally it is returned unchanged, but it may be altered by the
      transition method if necessary.

    Transition methods all return a 3-tuple:

    - A context object, as (potentially) modified by the transition method.
    - The next state name (a return value of ``None`` means no state change).
    - The processing result, a list, which is accumulated by the state
      machine.

    Transition methods may raise an `EOFError` to cut processing short.

    There are two implicit transitions, and corresponding transition methods
    are defined: `bof()` handles the beginning-of-file, and `eof()` handles
    the end-of-file. These methods have non-standard signatures and return
    values. `bof()` returns the initial context and results, and may be used
    to return a header string, or do any other processing needed. `eof()`
    should handle any remaining context and wrap things up; it returns the
    final processing result.

    Typical applications need only subclass `State` (or a subclass), set the
    `patterns` and `initial_transitions` class attributes, and provide
    corresponding transition methods. The default object initialization will
    take care of constructing the list of transitions.
    """

    patterns: ClassVar[dict[str, str | Pattern[str]] | None]
    initial_transitions: ClassVar[Sequence[str] | Sequence[tuple[str, str]] | None]
    nested_sm: type[StateMachine[_Context]]
    nested_sm_kwargs: dict[str, Any]
    transition_order: list[str]
    transitions: dict[str, tuple[Pattern[str], Callable[[], None], str]]
    state_machine: StateMachine[_Context]
    debug: bool
    def __init__(self, state_machine: StateMachine[_Context], debug: bool = False) -> None:
        """
        Initialize a `State` object; make & add initial transitions.

        Parameters:

        - `statemachine`: the controlling `StateMachine` object.
        - `debug`: a boolean; produce verbose output if true.
        """

    def runtime_init(self) -> None:
        """
        Initialize this `State` before running the state machine; called from
        `self.state_machine.run()`.
        """

    def unlink(self) -> None:
        """Remove circular references to objects no longer required."""

    def add_initial_transitions(self) -> None:
        """Make and add transitions listed in `self.initial_transitions`."""

    def add_transitions(self, names: Iterable[str], transitions) -> None:
        """
        Add a list of transitions to the start of the transition list.

        Parameters:

        - `names`: a list of transition names.
        - `transitions`: a mapping of names to transition tuples.

        Exceptions: `DuplicateTransitionError`, `UnknownTransitionError`.
        """

    def add_transition(self, name: str, transition: tuple[Pattern[str], str, str]) -> None:
        """
        Add a transition to the start of the transition list.

        Parameter `transition`: a ready-made transition 3-tuple.

        Exception: `DuplicateTransitionError`.
        """

    def remove_transition(self, name: str) -> None:
        """
        Remove a transition by `name`.

        Exception: `UnknownTransitionError`.
        """

    def make_transition(self, name: str, next_state: str | None = None) -> tuple[Pattern[str], _TransitionMethod[_Context], str]:
        """
        Make & return a transition tuple based on `name`.

        This is a convenience function to simplify transition creation.

        Parameters:

        - `name`: a string, the name of the transition pattern & method. This
          `State` object must have a method called '`name`', and a dictionary
          `self.patterns` containing a key '`name`'.
        - `next_state`: a string, the name of the next `State` object for this
          transition. A value of ``None`` (or absent) implies no state change
          (i.e., continue with the same state).

        Exceptions: `TransitionPatternNotFound`, `TransitionMethodNotFound`.
        """

    def make_transitions(
        self, name_list: list[str | tuple[str] | tuple[str, str]]
    ) -> tuple[list[str], dict[str, tuple[Pattern[str], _TransitionMethod[_Context], str]]]:
        """
        Return a list of transition names and a transition mapping.

        Parameter `name_list`: a list, where each entry is either a transition
        name string, or a 1- or 2-tuple (transition name, optional next state
        name).
        """

    def no_match(
        self, context: _Context, transitions: tuple[list[str], dict[str, tuple[Pattern[str], _TransitionMethod[_Context], str]]]
    ) -> _TransitionResult[_Context]:
        """
        Called when there is no match from `StateMachine.check_line()`.

        Return the same values returned by transition methods:

        - context: unchanged;
        - next state name: ``None``;
        - empty result list.

        Override in subclasses to catch this event.
        """

    def bof(self, context: _Context) -> tuple[list[str], list[str]]:
        """
        Handle beginning-of-file. Return unchanged `context`, empty result.

        Override in subclasses.

        Parameter `context`: application-defined storage.
        """

    def eof(self, context: _Context) -> list[str]:
        """
        Handle end-of-file. Return empty result.

        Override in subclasses.

        Parameter `context`: application-defined storage.
        """

    def nop(self, match: Match[str], context: _Context, next_state: str) -> _TransitionResult[_Context]:
        """
        A "do nothing" transition method.

        Return unchanged `context` & `next_state`, empty result. Useful for
        simple state changes (actionless transitions).
        """

class StateMachineWS(StateMachine[_Context]):
    """
    `StateMachine` subclass specialized for whitespace recognition.

    There are three methods provided for extracting indented text blocks:

    - `get_indented()`: use when the indent is unknown.
    - `get_known_indented()`: use when the indent is known for all lines.
    - `get_first_known_indented()`: use when only the first line's indent is
      known.
    """

    def get_indented(self, until_blank: bool = False, strip_indent: bool = True) -> tuple[StringList, int, int, bool]:
        """
        Return a block of indented lines of text, and info.

        Extract an indented block where the indent is unknown for all lines.

        :Parameters:
            - `until_blank`: Stop collecting at the first blank line if true.
            - `strip_indent`: Strip common leading indent if true (default).

        :Return:
            - the indented block (a list of lines of text),
            - its indent,
            - its first line offset from BOF, and
            - whether or not it finished with a blank line.
        """

    def get_known_indented(
        self, indent: int, until_blank: bool = False, strip_indent: bool = True
    ) -> tuple[list[str], int, bool]:
        """
        Return an indented block and info.

        Extract an indented block where the indent is known for all lines.
        Starting with the current line, extract the entire text block with at
        least `indent` indentation (which must be whitespace, except for the
        first line).

        :Parameters:
            - `indent`: The number of indent columns/characters.
            - `until_blank`: Stop collecting at the first blank line if true.
            - `strip_indent`: Strip `indent` characters of indentation if true
              (default).

        :Return:
            - the indented block,
            - its first line offset from BOF, and
            - whether or not it finished with a blank line.
        """

    def get_first_known_indented(
        self, indent: int, until_blank: bool = False, strip_indent: bool = True, strip_top: bool = True
    ) -> tuple[list[str], int, int, bool]:
        """
        Return an indented block and info.

        Extract an indented block where the indent is known for the first line
        and unknown for all other lines.

        :Parameters:
            - `indent`: The first line's indent (# of columns/characters).
            - `until_blank`: Stop collecting at the first blank line if true
              (1).
            - `strip_indent`: Strip `indent` characters of indentation if true
              (1, default).
            - `strip_top`: Strip blank lines from the beginning of the block.

        :Return:
            - the indented block,
            - its indent,
            - its first line offset from BOF, and
            - whether or not it finished with a blank line.
        """

class StateWS(State[_Context]):
    """
    State superclass specialized for whitespace (blank lines & indents).

    Use this class with `StateMachineWS`.  The transitions 'blank' (for blank
    lines) and 'indent' (for indented text blocks) are added automatically,
    before any other transitions.  The transition method `blank()` handles
    blank lines and `indent()` handles nested indented blocks.  Indented
    blocks trigger a new state machine to be created by `indent()` and run.
    The class of the state machine to be created is in `indent_sm`, and the
    constructor keyword arguments are in the dictionary `indent_sm_kwargs`.

    The methods `known_indent()` and `firstknown_indent()` are provided for
    indented blocks where the indent (all lines' and first line's only,
    respectively) is known to the transition method, along with the attributes
    `known_indent_sm` and `known_indent_sm_kwargs`.  Neither transition method
    is triggered automatically.
    """

    indent_sm: type[StateMachine[_Context]] | None
    indent_sm_kwargs: dict[str, Any] | None
    known_indent_sm: type[StateMachine[_Context]] | None
    known_indent_sm_kwargs: dict[str, Any] | None
    ws_patterns: dict[str, Pattern[str]]
    ws_initial_transitions: Sequence[str]
    def __init__(self, state_machine: StateMachine[_Context], debug: bool = False) -> None:
        """
        Initialize a `StateSM` object; extends `State.__init__()`.

        Check for indent state machine attributes, set defaults if not set.
        """

    def add_initial_transitions(self) -> None:
        """
        Add whitespace-specific transitions before those defined in subclass.

        Extends `State.add_initial_transitions()`.
        """

    def blank(self, match: Match[str], context: _Context, next_state: str) -> _TransitionResult[_Context]:
        """Handle blank lines. Does nothing. Override in subclasses."""

    def indent(self, match: Match[str], context: _Context, next_state: str) -> _TransitionResult[_Context]:
        """
        Handle an indented text block. Extend or override in subclasses.

        Recursively run the registered state machine for indented blocks
        (`self.indent_sm`).
        """

    def known_indent(self, match: Match[str], context: _Context, next_state: str) -> _TransitionResult[_Context]:
        """
        Handle a known-indent text block. Extend or override in subclasses.

        Recursively run the registered state machine for known-indent indented
        blocks (`self.known_indent_sm`). The indent is the length of the
        match, ``match.end()``.
        """

    def first_known_indent(self, match: Match[str], context: _Context, next_state: str) -> _TransitionResult[_Context]:
        """
        Handle an indented text block (first line's indent known).

        Extend or override in subclasses.

        Recursively run the registered state machine for known-indent indented
        blocks (`self.known_indent_sm`). The indent is the length of the
        match, ``match.end()``.
        """

class _SearchOverride:
    """
    Mix-in class to override `StateMachine` regular expression behavior.

    Changes regular expression matching, from the default `re.match()`
    (succeeds only if the pattern matches at the start of `self.line`) to
    `re.search()` (succeeds if the pattern matches anywhere in `self.line`).
    When subclassing a `StateMachine`, list this class **first** in the
    inheritance list of the class definition.
    """

    def match(self, pattern: Pattern[str]) -> Match[str]:
        """
        Return the result of a regular expression search.

        Overrides `StateMachine.match()`.

        Parameter `pattern`: `re` compiled regular expression.
        """

class SearchStateMachine(_SearchOverride, StateMachine[_Context]):
    """`StateMachine` which uses `re.search()` instead of `re.match()`."""

class SearchStateMachineWS(_SearchOverride, StateMachineWS[_Context]):
    """`StateMachineWS` which uses `re.search()` instead of `re.match()`."""

class ViewList(Generic[_T]):
    """
    List with extended functionality: slices of ViewList objects are child
    lists, linked to their parents. Changes made to a child list also affect
    the parent list.  A child list is effectively a "view" (in the SQL sense)
    of the parent list.  Changes to parent lists, however, do *not* affect
    active child lists.  If a parent list is changed, any active child lists
    should be recreated.

    The start and end of the slice can be trimmed using the `trim_start()` and
    `trim_end()` methods, without affecting the parent list.  The link between
    child and parent lists can be broken by calling `disconnect()` on the
    child list.

    Also, ViewList objects keep track of the source & offset of each item.
    This information is accessible via the `source()`, `offset()`, and
    `info()` methods.
    """

    data: list[_T]
    items: list[tuple[str, int]]
    parent: Self
    parent_offset: int
    def __init__(
        self,
        initlist: Self | Sequence[_T] | None = None,
        source: str | None = None,
        items: list[tuple[str, int]] | None = None,
        parent: Self | None = None,
        parent_offset: int | None = None,
    ) -> None: ...
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __contains__(self, item: _T) -> bool: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: slice) -> Self: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> _T: ...
    @overload
    def __setitem__(self, i: slice, item: Self) -> None: ...
    @overload
    def __setitem__(self, i: SupportsIndex, item: _T) -> None: ...
    def __delitem__(self, i: SupportsIndex) -> None: ...
    def __add__(self, other: Self) -> Self: ...
    def __radd__(self, other: Self) -> Self: ...
    def __iadd__(self, other: Self) -> Self: ...
    def __mul__(self, n: int) -> Self: ...
    __rmul__ = __mul__
    def __imul__(self, n: int) -> Self: ...
    def extend(self, other: Self) -> None: ...
    def append(self, item: _T, source: str | None = None, offset: int = 0) -> None: ...
    def insert(self, i: int, item: _T, source: str | None = None, offset: int = 0) -> None: ...
    def pop(self, i: int = -1) -> _T: ...
    def trim_start(self, n: int = 1) -> None:
        """
        Remove items from the start of the list, without touching the parent.
        """

    def trim_end(self, n: int = 1) -> None:
        """
        Remove items from the end of the list, without touching the parent.
        """

    def remove(self, item: _T) -> None: ...
    def count(self, item: _T) -> int: ...
    def index(self, item: _T) -> int: ...
    def reverse(self) -> None: ...
    def sort(self, *args: tuple[_T, tuple[str, int]]) -> None: ...
    def info(self, i: int) -> tuple[str, int | None]:
        """Return source & offset for index `i`."""

    def source(self, i: int) -> str:
        """Return source for index `i`."""

    def offset(self, i: int) -> int:
        """Return offset for index `i`."""

    def disconnect(self) -> None:
        """Break link between this list and parent list."""

    def xitems(self) -> Generator[tuple[str, int, str]]:
        """Return iterator yielding (source, offset, value) tuples."""

    def pprint(self) -> None:
        """Print the list in `grep` format (`source:offset:value` lines)"""
    # dummy atribute to indicate to mypy that ViewList is Iterable[str]
    def __iter__(self) -> Iterator[str]: ...

class StringList(ViewList[str]):
    """A `ViewList` with string-specific methods."""

    def trim_left(self, length: int, start: int = 0, end: int = sys.maxsize) -> None:
        """
        Trim `length` characters off the beginning of each item, in-place,
        from index `start` to `end`.  No whitespace-checking is done on the
        trimmed text.  Does not affect slice parent.
        """

    def get_text_block(self, start: int, flush_left: bool = False) -> StringList:
        """
        Return a contiguous block of text.

        If `flush_left` is true, raise `UnexpectedIndentationError` if an
        indented line is encountered before the text block ends (with a blank
        line).
        """

    def get_indented(
        self,
        start: int = 0,
        until_blank: bool = False,
        strip_indent: bool = True,
        block_indent: int | None = None,
        first_indent: int | None = None,
    ) -> tuple[StringList, int, bool]:
        """
        Extract and return a StringList of indented lines of text.

        Collect all lines with indentation, determine the minimum indentation,
        remove the minimum indentation from all indented lines (unless
        `strip_indent` is false), and return them. All lines up to but not
        including the first unindented line will be returned.

        :Parameters:
          - `start`: The index of the first line to examine.
          - `until_blank`: Stop collecting at the first blank line if true.
          - `strip_indent`: Strip common leading indent if true (default).
          - `block_indent`: The indent of the entire block, if known.
          - `first_indent`: The indent of the first line, if known.

        :Return:
          - a StringList of indented lines with minimum indent removed;
          - the amount of the indent;
          - a boolean: did the indented block finish with a blank line or EOF?
        """

    def get_2D_block(self, top: int, left: int, bottom: int, right: int, strip_indent: bool = True) -> StringList: ...
    def pad_double_width(self, pad_char: str) -> None:
        """Pad all double-width characters in `self` appending `pad_char`.

        For East Asian language support.
        """

    def replace(self, old: str, new: str) -> None:
        """Replace all occurrences of substring `old` with `new`."""

class StateMachineError(Exception): ...
class UnknownStateError(StateMachineError): ...
class DuplicateStateError(StateMachineError): ...
class UnknownTransitionError(StateMachineError): ...
class DuplicateTransitionError(StateMachineError): ...
class TransitionPatternNotFound(StateMachineError): ...
class TransitionMethodNotFound(StateMachineError): ...
class UnexpectedIndentationError(StateMachineError): ...

class TransitionCorrection(Exception):
    """
    Raise from within a transition method to switch to another transition.

    Raise with one argument, the new transition name.
    """

class StateCorrection(Exception):
    """
    Raise from within a transition method to switch to another state.

    Raise with one or two arguments: new state name, and an optional new
    transition name.
    """

def string2lines(astring: str, tab_width: int = 8, convert_whitespace: bool = False, whitespace: Pattern[str] = ...) -> list[str]:
    """
    Return a list of one-line strings with tabs expanded, no newlines, and
    trailing whitespace stripped.

    Each tab is expanded with between 1 and `tab_width` spaces, so that the
    next character's index becomes a multiple of `tab_width` (8 by default).

    Parameters:

    - `astring`: a multi-line string.
    - `tab_width`: the number of columns between tab stops.
    - `convert_whitespace`: convert form feeds and vertical tabs to spaces?
    - `whitespace`: pattern object with the to-be-converted
      whitespace characters (default [\\v\\f]).
    """
