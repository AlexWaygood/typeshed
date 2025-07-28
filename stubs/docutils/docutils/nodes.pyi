"""
Docutils document tree element class library.

Classes in CamelCase are abstract base classes or auxiliary classes. The one
exception is `Text`, for a text (PCDATA) node; uppercase is used to
differentiate from element classes.  Classes in lower_case_with_underscores
are element classes, matching the XML element generic identifiers in the DTD_.

The position of each node (the level at which it can occur) is significant and
is represented by abstract base classes (`Root`, `Structural`, `Body`,
`Inline`, etc.).  Certain transformations will be easier because we can use
``isinstance(node, base_class)`` to determine the position of the node in the
hierarchy.

.. _DTD: https://docutils.sourceforge.io/docs/ref/docutils.dtd
"""

import sys
import xml.dom.minidom
from abc import abstractmethod
from collections import Counter
from collections.abc import Callable, Generator, Iterable, Iterator, Mapping, Sequence
from typing import Any, ClassVar, Final, Literal, Protocol, SupportsIndex, TypeVar, overload
from typing_extensions import Self, TypeAlias

from docutils.frontend import Values
from docutils.transforms import Transform, Transformer
from docutils.utils import Reporter

_N = TypeVar("_N", bound=Node)

class _DomModule(Protocol):
    Document: type[xml.dom.minidom.Document]

__docformat__: Final = "reStructuredText"

# Functional Node Base Classes

class Node:
    """Abstract base class of nodes in a document tree."""

    # children is initialized by the subclasses
    children: Sequence[Node]
    # TODO: `parent` is actually `Element | None``, but `None`` only happens rarely,
    #       i.e. for synthetic nodes (or `document`, where it is overridden).
    #       See https://github.com/python/typeshed/blob/main/CONTRIBUTING.md#the-any-trick
    parent: Element | Any
    source: str | None
    line: int | None
    @property
    def document(self) -> document | None:
        """Return the `document` root node of the tree containing this Node."""

    @document.setter
    def document(self, value: document) -> None: ...
    def __bool__(self) -> Literal[True]:
        """
        Node instances are always true, even if they're empty.  A node is more
        than a simple container.  Its boolean "truth" does not depend on
        having one or more subnodes in the doctree.

        Use `len()` to check node length.
        """

    def asdom(self, dom: _DomModule | None = None) -> xml.dom.minidom.Element:
        """Return a DOM **fragment** representation of this Node."""
    # While docutils documents the Node class to be abstract it does not
    # actually use the ABCMeta metaclass. We still set @abstractmethod here
    # (although it's not used in the docutils implementation) because it
    # makes Mypy reject Node() with "Cannot instantiate abstract class".
    @abstractmethod
    def copy(self) -> Self:
        """Return a copy of self."""

    @abstractmethod
    def deepcopy(self) -> Self:
        """Return a deep copy of self (also copying children)."""

    @abstractmethod
    def pformat(self, indent: str = "    ", level: int = 0) -> str:
        """
        Return an indented pseudo-XML representation, for test purposes.

        Override in subclasses.
        """

    @abstractmethod
    def astext(self) -> str:
        """Return a string representation of this Node."""

    def setup_child(self, child: Node) -> None: ...
    def walk(self, visitor: NodeVisitor) -> bool:
        """
        Traverse a tree of `Node` objects, calling the
        `dispatch_visit()` method of `visitor` when entering each
        node.  (The `walkabout()` method is similar, except it also
        calls the `dispatch_departure()` method before exiting each
        node.)

        This tree traversal supports limited in-place tree
        modifications.  Replacing one node with one or more nodes is
        OK, as is removing an element.  However, if the node removed
        or replaced occurs after the current node, the old node will
        still be traversed, and any new nodes will not.

        Within ``visit`` methods (and ``depart`` methods for
        `walkabout()`), `TreePruningException` subclasses may be raised
        (`SkipChildren`, `SkipSiblings`, `SkipNode`, `SkipDeparture`).

        Parameter `visitor`: A `NodeVisitor` object, containing a
        ``visit`` implementation for each `Node` subclass encountered.

        Return true if we should stop the traversal.
        """

    def walkabout(self, visitor: NodeVisitor) -> bool:
        """
        Perform a tree traversal similarly to `Node.walk()` (which
        see), except also call the `dispatch_departure()` method
        before exiting each node.

        Parameter `visitor`: A `NodeVisitor` object, containing a
        ``visit`` and ``depart`` implementation for each `Node`
        subclass encountered.

        Return true if we should stop the traversal.
        """

    @overload
    def findall(
        self, condition: type[_N], include_self: bool = True, descend: bool = True, siblings: bool = False, ascend: bool = False
    ) -> Generator[_N, None, None]:
        """
        Return an iterator yielding nodes following `self`:

        * self (if `include_self` is true)
        * all descendants in tree traversal order (if `descend` is true)
        * the following siblings (if `siblings` is true) and their
          descendants (if also `descend` is true)
        * the following siblings of the parent (if `ascend` is true) and
          their descendants (if also `descend` is true), and so on.

        If `condition` is not None, the iterator yields only nodes
        for which ``condition(node)`` is true.  If `condition` is a
        node class ``cls``, it is equivalent to a function consisting
        of ``return isinstance(node, cls)``.

        If `ascend` is true, assume `siblings` to be true as well.

        If the tree structure is modified during iteration, the result
        is undefined.

        For example, given the following tree::

            <paragraph>
                <emphasis>      <--- emphasis.traverse() and
                    <strong>    <--- strong.traverse() are called.
                        Foo
                    Bar
                <reference name="Baz" refid="baz">
                    Baz

        Then tuple(emphasis.traverse()) equals ::

            (<emphasis>, <strong>, <#text: Foo>, <#text: Bar>)

        and list(strong.traverse(ascend=True) equals ::

            [<strong>, <#text: Foo>, <#text: Bar>, <reference>, <#text: Baz>]
        """

    @overload
    def findall(
        self,
        condition: Callable[[Node], bool] | None = None,
        include_self: bool = True,
        descend: bool = True,
        siblings: bool = False,
        ascend: bool = False,
    ) -> Generator[Node, None, None]: ...
    @overload
    def traverse(
        self, condition: type[_N], include_self: bool = True, descend: bool = True, siblings: bool = False, ascend: bool = False
    ) -> list[_N]:
        """Return list of nodes following `self`.

        For looping, Node.findall() is faster and more memory efficient.
        """

    @overload
    def traverse(
        self,
        condition: Callable[[Node], bool] | None = None,
        include_self: bool = True,
        descend: bool = True,
        siblings: bool = False,
        ascend: bool = False,
    ) -> list[Node]: ...
    @overload
    def next_node(
        self, condition: type[_N], include_self: bool = False, descend: bool = True, siblings: bool = False, ascend: bool = False
    ) -> _N:
        """
        Return the first node in the iterator returned by findall(),
        or None if the iterable is empty.

        Parameter list is the same as of `findall()`.  Note that `include_self`
        defaults to False, though.
        """

    @overload
    def next_node(
        self,
        condition: Callable[[Node], bool] | None = None,
        include_self: bool = False,
        descend: bool = True,
        siblings: bool = False,
        ascend: bool = False,
    ) -> Node: ...

# Left out
# - def ensure_str (deprecated)
# - def unescape (canonical import from docutils.utils)
def unescape(text: str, restore_backslashes: bool = False, respect_whitespace: bool = False) -> str:
    """
    Return a string with nulls removed or restored to backslashes.
    Backslash-escaped spaces are also removed.
    """

class Text(Node, str):
    """
    Instances are terminal nodes (leaves) containing text only; no child
    nodes or attributes.  Initialize by passing a string to the constructor.

    Access the raw (null-escaped) text with ``str(<instance>)``
    and unescaped text with ``<instance>.astext()``.
    """

    tagname: ClassVar[str]
    children: tuple[()]

    # we omit the rawsource parameter because it has been deprecated and is ignored
    def __new__(cls, data: str) -> Self:
        """Assert that `data` is not an array of bytes
        and warn if the deprecated `rawsource` argument is used.
        """

    def __init__(self, data: str) -> None: ...
    def shortrepr(self, maxlen: int = 18) -> str: ...
    def copy(self) -> Self: ...
    def deepcopy(self) -> Self: ...
    def pformat(self, indent: str = "    ", level: int = 0) -> str: ...
    def astext(self) -> str: ...
    def rstrip(self, chars: str | None = None) -> str: ...
    def lstrip(self, chars: str | None = None) -> str: ...

_T = TypeVar("_T")

class Element(Node):
    """
    `Element` is the superclass to all specific elements.

    Elements contain attributes and child nodes.
    They can be described as a cross between a list and a dictionary.

    Elements emulate dictionaries for external [#]_ attributes, indexing by
    attribute name (a string). To set the attribute 'att' to 'value', do::

        element['att'] = 'value'

    .. [#] External attributes correspond to the XML element attributes.
       From its `Node` superclass, Element also inherits "internal"
       class attributes that are accessed using the standard syntax, e.g.
       ``element.parent``.

    There are two special attributes: 'ids' and 'names'.  Both are
    lists of unique identifiers: 'ids' conform to the regular expression
    ``[a-z](-?[a-z0-9]+)*`` (see the make_id() function for rationale and
    details). 'names' serve as user-friendly interfaces to IDs; they are
    case- and whitespace-normalized (see the fully_normalize_name() function).

    Elements emulate lists for child nodes (element nodes and/or text
    nodes), indexing by integer.  To get the first child node, use::

        element[0]

    to iterate over the child nodes (without descending), use::

        for child in element:
            ...

    Elements may be constructed using the ``+=`` operator.  To add one new
    child node to element, do::

        element += node

    This is equivalent to ``element.append(node)``.

    To add a list of multiple child nodes at once, use the same ``+=``
    operator::

        element += [node1, node2]

    This is equivalent to ``element.extend([node1, node2])``.
    """

    local_attributes: ClassVar[Sequence[str]]
    basic_attributes: ClassVar[Sequence[str]]
    list_attributes: ClassVar[Sequence[str]]
    known_attributes: ClassVar[Sequence[str]]
    tagname: str
    child_text_separator: ClassVar[str]
    attributes: dict[str, Any]
    children: list[Node]
    rawsource: str
    def __init__(self, rawsource: str = "", *children: Node, **attributes: Any) -> None: ...
    def shortrepr(self) -> str: ...
    def starttag(self, quoteattr: Callable[[str], str] | None = None) -> str: ...
    def endtag(self) -> str: ...
    def emptytag(self) -> str: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: str | Node) -> bool: ...
    @overload
    def __getitem__(self, key: str) -> Any: ...
    @overload
    def __getitem__(self, key: int) -> Node: ...
    @overload
    def __getitem__(self, key: slice) -> list[Node]: ...
    @overload
    def __setitem__(self, key: str, item: Any) -> None: ...
    @overload
    def __setitem__(self, key: int, item: Node) -> None: ...
    @overload
    def __setitem__(self, key: slice, item: Iterable[Node]) -> None: ...
    def __delitem__(self, key: str | int | slice) -> None: ...
    def __add__(self, other: list[Node]) -> list[Node]: ...
    def __radd__(self, other: list[Node]) -> list[Node]: ...
    def __iadd__(self, other: Node | Iterable[Node]) -> Self:
        """Append a node or a list of nodes to `self.children`."""

    def astext(self) -> str: ...
    def non_default_attributes(self) -> dict[str, Any]: ...
    def attlist(self) -> list[tuple[str, Any]]: ...
    @overload
    def get(self, key: str) -> Any: ...
    @overload
    def get(self, key: str, failobj: _T) -> _T: ...
    def hasattr(self, attr: str) -> bool: ...
    def delattr(self, attr: str) -> None: ...
    @overload
    def setdefault(self, key: str) -> Any: ...
    @overload
    def setdefault(self, key: str, failobj: _T) -> Any | _T: ...
    has_key = hasattr
    def get_language_code(self, fallback: str = "") -> str:
        """Return node's language tag.

        Look iteratively in self and parents for a class argument
        starting with ``language-`` and return the remainder of it
        (which should be a `BCP49` language tag) or the `fallback`.
        """

    def append(self, item: Node) -> None: ...
    def extend(self, item: Iterable[Node]) -> None: ...
    def insert(self, index: SupportsIndex, item: Node | Iterable[Node] | None) -> None: ...
    def pop(self, i: int = -1) -> Node: ...
    def remove(self, item: Node) -> None: ...
    def index(self, item: Node, start: int = 0, stop: int = sys.maxsize) -> int: ...
    def previous_sibling(self) -> Node | None:
        """Return preceding sibling node or ``None``."""

    def is_not_default(self, key: str) -> bool: ...
    def update_basic_atts(self, dict_: Mapping[str, Any] | Node) -> None:
        """
        Update basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') from node or dictionary `dict_`.
        """

    def append_attr_list(self, attr: str, values: Iterable[Any]) -> None:
        """
        For each element in values, if it does not exist in self[attr], append
        it.

        NOTE: Requires self[attr] and values to be sequence type and the
        former should specifically be a list.
        """

    def coerce_append_attr_list(self, attr: str, value) -> None:
        """
        First, convert both self[attr] and value to a non-string sequence
        type; if either is not already a sequence, convert it to a list of one
        element.  Then call append_attr_list.

        NOTE: self[attr] and value both must not be None.
        """

    def replace_attr(self, attr: str, value: Any, force: bool = True) -> None:
        """
        If self[attr] does not exist or force is True or omitted, set
        self[attr] to value, otherwise do nothing.
        """

    def copy_attr_convert(self, attr: str, value: Any, replace: bool = True) -> None:
        """
        If attr is an attribute of self, set self[attr] to
        [self[attr], value], otherwise set self[attr] to value.

        NOTE: replace is not used by this function and is kept only for
              compatibility with the other copy functions.
        """

    def copy_attr_coerce(self, attr: str, value: Any, replace: bool) -> None:
        """
        If attr is an attribute of self and either self[attr] or value is a
        list, convert all non-sequence values to a sequence of 1 element and
        then concatenate the two sequence, setting the result to self[attr].
        If both self[attr] and value are non-sequences and replace is True or
        self[attr] is None, replace self[attr] with value. Otherwise, do
        nothing.
        """

    def copy_attr_concatenate(self, attr: str, value: Any, replace: bool) -> None:
        """
        If attr is an attribute of self and both self[attr] and value are
        lists, concatenate the two sequences, setting the result to
        self[attr].  If either self[attr] or value are non-sequences and
        replace is True or self[attr] is None, replace self[attr] with value.
        Otherwise, do nothing.
        """

    def copy_attr_consistent(self, attr: str, value: Any, replace: bool) -> None:
        """
        If replace is True or self[attr] is None, replace self[attr] with
        value.  Otherwise, do nothing.
        """

    def update_all_atts(
        self,
        dict_: Mapping[str, Any] | Node,
        update_fun: Callable[[Element, str, Any, bool], object] = ...,
        replace: bool = True,
        and_source: bool = False,
    ) -> None:
        """
        Updates all attributes from node or dictionary `dict_`.

        Appends the basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') and then, for all other attributes in
        dict_, updates the same attribute in self.  When attributes with the
        same identifier appear in both self and dict_, the two values are
        merged based on the value of update_fun.  Generally, when replace is
        True, the values in self are replaced or merged with the values in
        dict_; otherwise, the values in self may be preserved or merged.  When
        and_source is True, the 'source' attribute is included in the copy.

        NOTE: When replace is False, and self contains a 'source' attribute,
              'source' is not replaced even when dict_ has a 'source'
              attribute, though it may still be merged into a list depending
              on the value of update_fun.
        NOTE: It is easier to call the update-specific methods then to pass
              the update_fun method to this function.
        """

    def update_all_atts_consistantly(
        self, dict_: Mapping[str, Any] | Node, replace: bool = True, and_source: bool = False
    ) -> None:
        """
        Updates all attributes from node or dictionary `dict_`.

        Appends the basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') and then, for all other attributes in
        dict_, updates the same attribute in self.  When attributes with the
        same identifier appear in both self and dict_ and replace is True, the
        values in self are replaced with the values in dict_; otherwise, the
        values in self are preserved.  When and_source is True, the 'source'
        attribute is included in the copy.

        NOTE: When replace is False, and self contains a 'source' attribute,
              'source' is not replaced even when dict_ has a 'source'
              attribute, though it may still be merged into a list depending
              on the value of update_fun.
        """

    def update_all_atts_concatenating(self, dict_: dict[str, Any] | Node, replace: bool = True, and_source: bool = False) -> None:
        """
        Updates all attributes from node or dictionary `dict_`.

        Appends the basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') and then, for all other attributes in
        dict_, updates the same attribute in self.  When attributes with the
        same identifier appear in both self and dict_ whose values aren't each
        lists and replace is True, the values in self are replaced with the
        values in dict_; if the values from self and dict_ for the given
        identifier are both of list type, then the two lists are concatenated
        and the result stored in self; otherwise, the values in self are
        preserved.  When and_source is True, the 'source' attribute is
        included in the copy.

        NOTE: When replace is False, and self contains a 'source' attribute,
              'source' is not replaced even when dict_ has a 'source'
              attribute, though it may still be merged into a list depending
              on the value of update_fun.
        """

    def update_all_atts_coercion(self, dict_: Mapping[str, Any] | Node, replace: bool = True, and_source: bool = False) -> None:
        """
        Updates all attributes from node or dictionary `dict_`.

        Appends the basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') and then, for all other attributes in
        dict_, updates the same attribute in self.  When attributes with the
        same identifier appear in both self and dict_ whose values are both
        not lists and replace is True, the values in self are replaced with
        the values in dict_; if either of the values from self and dict_ for
        the given identifier are of list type, then first any non-lists are
        converted to 1-element lists and then the two lists are concatenated
        and the result stored in self; otherwise, the values in self are
        preserved.  When and_source is True, the 'source' attribute is
        included in the copy.

        NOTE: When replace is False, and self contains a 'source' attribute,
              'source' is not replaced even when dict_ has a 'source'
              attribute, though it may still be merged into a list depending
              on the value of update_fun.
        """

    def update_all_atts_convert(self, dict_: Mapping[str, Any] | Node, and_source: bool = False) -> None:
        """
        Updates all attributes from node or dictionary `dict_`.

        Appends the basic attributes ('ids', 'names', 'classes',
        'dupnames', but not 'source') and then, for all other attributes in
        dict_, updates the same attribute in self.  When attributes with the
        same identifier appear in both self and dict_ then first any non-lists
        are converted to 1-element lists and then the two lists are
        concatenated and the result stored in self; otherwise, the values in
        self are preserved.  When and_source is True, the 'source' attribute
        is included in the copy.

        NOTE: When replace is False, and self contains a 'source' attribute,
              'source' is not replaced even when dict_ has a 'source'
              attribute, though it may still be merged into a list depending
              on the value of update_fun.
        """

    def clear(self) -> None: ...
    def replace(self, old: Node, new: Node | Sequence[Node]) -> None:
        """Replace one child `Node` with another child or children."""

    def replace_self(self, new: Node | Sequence[Node]) -> None:
        """
        Replace `self` node with `new`, where `new` is a node or a
        list of nodes.
        """

    def first_child_matching_class(
        self, childclass: type[Node] | tuple[type[Node], ...], start: int = 0, end: int = sys.maxsize
    ) -> int | None:
        """
        Return the index of the first child whose class exactly matches.

        Parameters:

        - `childclass`: A `Node` subclass to search for, or a tuple of `Node`
          classes. If a tuple, any of the classes may match.
        - `start`: Initial index to check.
        - `end`: Initial index to *not* check.
        """

    def first_child_not_matching_class(
        self, childclass: type[Node] | tuple[type[Node], ...], start: int = 0, end: int = sys.maxsize
    ) -> int | None:
        """
        Return the index of the first child whose class does *not* match.

        Parameters:

        - `childclass`: A `Node` subclass to skip, or a tuple of `Node`
          classes. If a tuple, none of the classes may match.
        - `start`: Initial index to check.
        - `end`: Initial index to *not* check.
        """

    def pformat(self, indent: str = "    ", level: int = 0) -> str: ...
    def copy(self) -> Self: ...
    def deepcopy(self) -> Self: ...
    def set_class(self, name: str) -> None:
        """Add a new class to the "classes" attribute."""

    def note_referenced_by(self, name: str | None = None, id: str | None = None) -> None:
        """Note that this Element has been referenced by its name
        `name` or id `id`.
        """

    @classmethod
    def is_not_list_attribute(cls, attr: str) -> bool:
        """
        Returns True if and only if the given attribute is NOT one of the
        basic list attributes defined for all Elements.
        """

    @classmethod
    def is_not_known_attribute(cls, attr: str) -> bool:
        """
        Returns True if and only if the given attribute is NOT recognized by
        this class.
        """
    # '__iter__' is added as workaround, since mypy doesn't support classes that are iterable via '__getitem__'
    # see https://github.com/python/typeshed/pull/10099#issuecomment-1528789395
    def __iter__(self) -> Iterator[Node]: ...

class TextElement(Element):
    """
    An element which directly contains text.

    Its children are all `Text` or `Inline` subclass nodes.  You can
    check whether an element's context is inline simply by checking whether
    its immediate parent is a `TextElement` instance (including subclasses).
    This is handy for nodes like `image` that can appear both inline and as
    standalone body elements.

    If passing children to `__init__()`, make sure to set `text` to
    ``''`` or some other suitable value.
    """

    def __init__(self, rawsource: str = "", text: str = "", *children: Node, **attributes) -> None: ...

class FixedTextElement(TextElement):
    """An element which directly contains preformatted text."""

# Mixins

class Resolvable:
    resolved: int

class BackLinkable:
    def add_backref(self, refid: str) -> None: ...

# Element Categories

class Root: ...
class Titular: ...

class PreBibliographic:
    """Category of Node which may occur before Bibliographic Nodes."""

class Bibliographic: ...
class Decorative(PreBibliographic): ...
class Structural: ...
class Body: ...
class General(Body): ...

class Sequential(Body):
    """List-like elements."""

class Admonition(Body): ...

class Special(Body):
    """Special internal body elements."""

class Invisible(PreBibliographic):
    """Internal elements that don't appear in output."""

class Part: ...
class Inline: ...
class Referential(Resolvable): ...

class Targetable(Resolvable):
    referenced: int
    indirect_reference_name: str | None

class Labeled:
    """Contains a `label` as its first element."""

# Root Element

_Document: TypeAlias = document
_Decoration: TypeAlias = decoration

class document(Root, Structural, Element):
    """
    The document root element.

    Do not instantiate this class directly; use
    `docutils.utils.new_document()` instead.
    """

    current_source: str | None
    current_line: int | None
    settings: Values
    reporter: Reporter
    indirect_targets: list[target]
    substitution_defs: dict[str, substitution_definition]
    substitution_names: dict[str, str]
    refnames: dict[str, list[Element]]
    refids: dict[str, list[Element]]
    nameids: dict[str, str]
    nametypes: dict[str, bool]
    ids: dict[str, Element]
    footnote_refs: dict[str, list[footnote_reference]]
    citation_refs: dict[str, list[citation_reference]]
    autofootnotes: list[footnote]
    autofootnote_refs: list[footnote_reference]
    symbol_footnotes: list[footnote]
    symbol_footnote_refs: list[footnote_reference]
    footnotes: list[footnote]
    citations: list[citation]
    autofootnote_start: int
    symbol_footnote_start: int
    id_counter: Counter[int]
    parse_messages: list[system_message]
    transform_messages: list[system_message]
    transformer: Transformer
    decoration: decoration | None
    document: Self
    def __init__(self, settings: Values, reporter: Reporter, *args: Node, **kwargs: Any) -> None: ...
    def asdom(self, dom: Any | None = None) -> Any:
        """Return a DOM representation of this document."""

    def set_id(self, node: Element, msgnode: Element | None = None, suggested_prefix: str = "") -> str: ...
    def set_name_id_map(self, node: Element, id: str, msgnode: Element | None = None, explicit: bool | None = None) -> None:
        """
        `self.nameids` maps names to IDs, while `self.nametypes` maps names to
        booleans representing hyperlink type (True==explicit,
        False==implicit).  This method updates the mappings.

        The following state transition table shows how `self.nameids` items
        ("id") and `self.nametypes` items ("type") change with new input
        (a call to this method), and what actions are performed
        ("implicit"-type system messages are INFO/1, and
        "explicit"-type system messages are ERROR/3):

        ====  =====  ========  ========  =======  ====  =====  =====
         Old State    Input          Action        New State   Notes
        -----------  --------  -----------------  -----------  -----
        id    type   new type  sys.msg.  dupname  id    type
        ====  =====  ========  ========  =======  ====  =====  =====
        -     -      explicit  -         -        new   True
        -     -      implicit  -         -        new   False
        -     False  explicit  -         -        new   True
        old   False  explicit  implicit  old      new   True
        -     True   explicit  explicit  new      -     True
        old   True   explicit  explicit  new,old  -     True   [#]_
        -     False  implicit  implicit  new      -     False
        old   False  implicit  implicit  new,old  -     False
        -     True   implicit  implicit  new      -     True
        old   True   implicit  implicit  new      old   True
        ====  =====  ========  ========  =======  ====  =====  =====

        .. [#] Do not clear the name-to-id map or invalidate the old target if
           both old and new targets are external and refer to identical URIs.
           The new target is invalidated regardless.
        """

    def set_duplicate_name_id(self, node: Element, id: str, name: str, msgnode: Element, explicit: bool) -> None: ...
    def has_name(self, name: str) -> bool: ...
    def note_implicit_target(self, target: Element, msgnode: Element | None = None) -> None: ...
    def note_explicit_target(self, target: Element, msgnode: Element | None = None) -> None: ...
    def note_refname(self, node: Element) -> None: ...
    def note_refid(self, node: Element) -> None: ...
    def note_indirect_target(self, target: target) -> None: ...
    def note_anonymous_target(self, target: target) -> None: ...
    def note_autofootnote(self, footnote: footnote) -> None: ...
    def note_autofootnote_ref(self, ref: footnote_reference) -> None: ...
    def note_symbol_footnote(self, footnote: footnote) -> None: ...
    def note_symbol_footnote_ref(self, ref: footnote_reference) -> None: ...
    def note_footnote(self, footnote: footnote) -> None: ...
    def note_footnote_ref(self, ref: footnote_reference) -> None: ...
    def note_citation(self, citation: citation) -> None: ...
    def note_citation_ref(self, ref: citation_reference) -> None: ...
    def note_substitution_def(self, subdef: substitution_definition, def_name: str, msgnode: Element | None = None) -> None: ...
    def note_substitution_ref(self, subref: substitution_reference, refname: str) -> None: ...
    def note_pending(self, pending: pending, priority: int | None = None) -> None: ...
    def note_parse_message(self, message: system_message) -> None: ...
    def note_transform_message(self, message: system_message) -> None: ...
    def note_source(self, source: str, offset: int) -> None: ...
    def copy(self) -> Self: ...
    def get_decoration(self) -> _Decoration: ...

# Title Elements

class title(Titular, PreBibliographic, TextElement): ...
class subtitle(Titular, PreBibliographic, TextElement): ...
class rubric(Titular, TextElement): ...

# Meta-Data Element

class meta(PreBibliographic, Element):
    """Container for "invisible" bibliographic data, or meta-data."""

# Bibliographic Elements

class docinfo(Bibliographic, Element): ...
class author(Bibliographic, TextElement): ...
class authors(Bibliographic, Element): ...
class organization(Bibliographic, TextElement): ...
class address(Bibliographic, FixedTextElement): ...
class contact(Bibliographic, TextElement): ...
class version(Bibliographic, TextElement): ...
class revision(Bibliographic, TextElement): ...
class status(Bibliographic, TextElement): ...
class date(Bibliographic, TextElement): ...
class copyright(Bibliographic, TextElement): ...

# Decorative Elements

class decoration(Decorative, Element):
    def get_header(self) -> header: ...
    def get_footer(self) -> footer: ...

class header(Decorative, Element): ...
class footer(Decorative, Element): ...

# Structural Elements

class section(Structural, Element): ...

class topic(Structural, Element):
    """
    Topics are terminal, "leaf" mini-sections, like block quotes with titles,
    or textual figures.  A topic is just like a section, except that it has no
    subsections, and it doesn't have to conform to section placement rules.

    Topics are allowed wherever body elements (list, table, etc.) are allowed,
    but only at the top level of a section or document.  Topics cannot nest
    inside topics, sidebars, or body elements; you can't have a topic inside a
    table, list, block quote, etc.
    """

class sidebar(Structural, Element):
    """
    Sidebars are like miniature, parallel documents that occur inside other
    documents, providing related or reference material.  A sidebar is
    typically offset by a border and "floats" to the side of the page; the
    document's main text may flow around it.  Sidebars can also be likened to
    super-footnotes; their content is outside of the flow of the document's
    main text.

    Sidebars are allowed wherever body elements (list, table, etc.) are
    allowed, but only at the top level of a section or document.  Sidebars
    cannot nest inside sidebars, topics, or body elements; you can't have a
    sidebar inside a table, list, block quote, etc.
    """

class transition(Structural, Element): ...

# Body Elements
# ===============

class paragraph(General, TextElement): ...
class compound(General, Element): ...
class container(General, Element): ...
class bullet_list(Sequential, Element): ...
class enumerated_list(Sequential, Element): ...
class list_item(Part, Element): ...
class definition_list(Sequential, Element): ...
class definition_list_item(Part, Element): ...
class term(Part, TextElement): ...
class classifier(Part, TextElement): ...
class definition(Part, Element): ...
class field_list(Sequential, Element): ...
class field(Part, Element): ...
class field_name(Part, TextElement): ...
class field_body(Part, Element): ...
class option(Part, Element): ...
class option_argument(Part, TextElement): ...
class option_group(Part, Element): ...
class option_list(Sequential, Element): ...
class option_list_item(Part, Element): ...
class option_string(Part, TextElement): ...
class description(Part, Element): ...
class literal_block(General, FixedTextElement): ...
class doctest_block(General, FixedTextElement): ...
class math_block(General, FixedTextElement): ...
class line_block(General, Element): ...

class line(Part, TextElement):
    indent: str | None

class block_quote(General, Element): ...
class attribution(Part, TextElement): ...
class attention(Admonition, Element): ...
class caution(Admonition, Element): ...
class danger(Admonition, Element): ...
class error(Admonition, Element): ...
class important(Admonition, Element): ...
class note(Admonition, Element): ...
class tip(Admonition, Element): ...
class hint(Admonition, Element): ...
class warning(Admonition, Element): ...
class admonition(Admonition, Element): ...
class comment(Special, Invisible, FixedTextElement): ...
class substitution_definition(Special, Invisible, TextElement): ...
class target(Special, Invisible, Inline, TextElement, Targetable): ...
class footnote(General, BackLinkable, Element, Labeled, Targetable): ...
class citation(General, BackLinkable, Element, Labeled, Targetable): ...
class label(Part, TextElement): ...
class figure(General, Element): ...
class caption(Part, TextElement): ...
class legend(Part, Element): ...
class table(General, Element): ...
class tgroup(Part, Element): ...
class colspec(Part, Element): ...
class thead(Part, Element): ...
class tbody(Part, Element): ...
class row(Part, Element): ...
class entry(Part, Element): ...

class system_message(Special, BackLinkable, PreBibliographic, Element):
    """
    System message element.

    Do not instantiate this class directly; use
    ``document.reporter.info/warning/error/severe()`` instead.
    """

    def __init__(self, message: str | None = None, *children: Node, **attributes) -> None: ...
    def astext(self) -> str: ...

class pending(Special, Invisible, Element):
    """
    The "pending" element is used to encapsulate a pending operation: the
    operation (transform), the point at which to apply it, and any data it
    requires.  Only the pending operation's location within the document is
    stored in the public document tree (by the "pending" object itself); the
    operation and its data are stored in the "pending" object's internal
    instance attributes.

    For example, say you want a table of contents in your reStructuredText
    document.  The easiest way to specify where to put it is from within the
    document, with a directive::

        .. contents::

    But the "contents" directive can't do its work until the entire document
    has been parsed and possibly transformed to some extent.  So the directive
    code leaves a placeholder behind that will trigger the second phase of its
    processing, something like this::

        <pending ...public attributes...> + internal attributes

    Use `document.note_pending()` so that the
    `docutils.transforms.Transformer` stage of processing can run all pending
    transforms.
    """

    transform: type[Transform]
    details: Mapping[str, Any]
    def __init__(
        self,
        transform: type[Transform],
        details: Mapping[str, Any] | None = None,
        rawsource: str = "",
        *children: Node,
        **attributes,
    ) -> None: ...

class raw(Special, Inline, PreBibliographic, FixedTextElement):
    """
    Raw data that is to be passed untouched to the Writer.
    """

# Inline Elements

class emphasis(Inline, TextElement): ...
class strong(Inline, TextElement): ...
class literal(Inline, TextElement): ...
class reference(General, Inline, Referential, TextElement): ...
class footnote_reference(Inline, Referential, TextElement): ...
class citation_reference(Inline, Referential, TextElement): ...
class substitution_reference(Inline, TextElement): ...
class title_reference(Inline, TextElement): ...
class abbreviation(Inline, TextElement): ...
class acronym(Inline, TextElement): ...
class superscript(Inline, TextElement): ...
class subscript(Inline, TextElement): ...
class math(Inline, TextElement): ...
class image(General, Inline, Element): ...
class inline(Inline, TextElement): ...
class problematic(Inline, TextElement): ...
class generated(Inline, TextElement): ...

# Auxiliary Classes, Functions, and Data

node_class_names: list[str]

class NodeVisitor:
    """
    "Visitor" pattern [GoF95]_ abstract superclass implementation for
    document tree traversals.

    Each node class has corresponding methods, doing nothing by
    default; override individual methods for specific and useful
    behaviour.  The `dispatch_visit()` method is called by
    `Node.walk()` upon entering a node.  `Node.walkabout()` also calls
    the `dispatch_departure()` method before exiting a node.

    The dispatch methods call "``visit_`` + node class name" or
    "``depart_`` + node class name", resp.

    This is a base class for visitors whose ``visit_...`` & ``depart_...``
    methods must be implemented for *all* compulsory node types encountered
    (such as for `docutils.writers.Writer` subclasses).
    Unimplemented methods will raise exceptions (except for optional nodes).

    For sparse traversals, where only certain node types are of interest, use
    subclass `SparseNodeVisitor` instead.  When (mostly or entirely) uniform
    processing is desired, subclass `GenericNodeVisitor`.

    .. [GoF95] Gamma, Helm, Johnson, Vlissides. *Design Patterns: Elements of
       Reusable Object-Oriented Software*. Addison-Wesley, Reading, MA, USA,
       1995.
    """

    optional: ClassVar[tuple[str, ...]]
    document: _Document
    def __init__(self, document: _Document) -> None: ...
    def dispatch_visit(self, node: Node) -> Any:
        """
        Call self."``visit_`` + node class name" with `node` as
        parameter.  If the ``visit_...`` method does not exist, call
        self.unknown_visit.
        """

    def dispatch_departure(self, node: Node) -> Any:
        """
        Call self."``depart_`` + node class name" with `node` as
        parameter.  If the ``depart_...`` method does not exist, call
        self.unknown_departure.
        """

    def unknown_visit(self, node: Node) -> Any:
        """
        Called when entering unknown `Node` types.

        Raise an exception unless overridden.
        """

    def unknown_departure(self, node: Node) -> Any:
        """
        Called before exiting unknown `Node` types.

        Raise exception unless overridden.
        """
    # These methods only exist on the subclasses `GenericNodeVisitor` and `SparseNodeVisitor` at runtime.
    # If subclassing `NodeVisitor` directly, `visit_*` methods must be implemented for nodes and children that will be called
    # with `Node.walk()` and `Node.walkabout()`.
    # `depart_*` methods must also be implemented for nodes and children that will be called with `Node.walkabout()`.
    def visit_Text(self, node: Text) -> Any: ...
    def visit_abbreviation(self, node: abbreviation) -> Any: ...
    def visit_acronym(self, node: acronym) -> Any: ...
    def visit_address(self, node: address) -> Any: ...
    def visit_admonition(self, node: admonition) -> Any: ...
    def visit_attention(self, node: attention) -> Any: ...
    def visit_attribution(self, node: attribution) -> Any: ...
    def visit_author(self, node: author) -> Any: ...
    def visit_authors(self, node: authors) -> Any: ...
    def visit_block_quote(self, node: block_quote) -> Any: ...
    def visit_bullet_list(self, node: bullet_list) -> Any: ...
    def visit_caption(self, node: caption) -> Any: ...
    def visit_caution(self, node: caution) -> Any: ...
    def visit_citation(self, node: citation) -> Any: ...
    def visit_citation_reference(self, node: citation_reference) -> Any: ...
    def visit_classifier(self, node: classifier) -> Any: ...
    def visit_colspec(self, node: colspec) -> Any: ...
    def visit_comment(self, node: comment) -> Any: ...
    def visit_compound(self, node: compound) -> Any: ...
    def visit_contact(self, node: contact) -> Any: ...
    def visit_container(self, node: container) -> Any: ...
    def visit_copyright(self, node: copyright) -> Any: ...
    def visit_danger(self, node: danger) -> Any: ...
    def visit_date(self, node: date) -> Any: ...
    def visit_decoration(self, node: decoration) -> Any: ...
    def visit_definition(self, node: definition) -> Any: ...
    def visit_definition_list(self, node: definition_list) -> Any: ...
    def visit_definition_list_item(self, node: definition_list_item) -> Any: ...
    def visit_description(self, node: description) -> Any: ...
    def visit_docinfo(self, node: docinfo) -> Any: ...
    def visit_doctest_block(self, node: doctest_block) -> Any: ...
    def visit_document(self, node: _Document) -> Any: ...
    def visit_emphasis(self, node: emphasis) -> Any: ...
    def visit_entry(self, node: entry) -> Any: ...
    def visit_enumerated_list(self, node: enumerated_list) -> Any: ...
    def visit_error(self, node: error) -> Any: ...
    def visit_field(self, node: field) -> Any: ...
    def visit_field_body(self, node: field_body) -> Any: ...
    def visit_field_list(self, node: field_list) -> Any: ...
    def visit_field_name(self, node: field_name) -> Any: ...
    def visit_figure(self, node: figure) -> Any: ...
    def visit_footer(self, node: footer) -> Any: ...
    def visit_footnote(self, node: footnote) -> Any: ...
    def visit_footnote_reference(self, node: footnote_reference) -> Any: ...
    def visit_generated(self, node: generated) -> Any: ...
    def visit_header(self, node: header) -> Any: ...
    def visit_hint(self, node: hint) -> Any: ...
    def visit_image(self, node: image) -> Any: ...
    def visit_important(self, node: important) -> Any: ...
    def visit_inline(self, node: inline) -> Any: ...
    def visit_label(self, node: label) -> Any: ...
    def visit_legend(self, node: legend) -> Any: ...
    def visit_line(self, node: line) -> Any: ...
    def visit_line_block(self, node: line_block) -> Any: ...
    def visit_list_item(self, node: list_item) -> Any: ...
    def visit_literal(self, node: literal) -> Any: ...
    def visit_literal_block(self, node: literal_block) -> Any: ...
    def visit_math(self, node: math) -> Any: ...
    def visit_math_block(self, node: math_block) -> Any: ...
    def visit_meta(self, node: meta) -> Any: ...
    def visit_note(self, node: note) -> Any: ...
    def visit_option(self, node: option) -> Any: ...
    def visit_option_argument(self, node: option_argument) -> Any: ...
    def visit_option_group(self, node: option_group) -> Any: ...
    def visit_option_list(self, node: option_list) -> Any: ...
    def visit_option_list_item(self, node: option_list_item) -> Any: ...
    def visit_option_string(self, node: option_string) -> Any: ...
    def visit_organization(self, node: organization) -> Any: ...
    def visit_paragraph(self, node: paragraph) -> Any: ...
    def visit_pending(self, node: pending) -> Any: ...
    def visit_problematic(self, node: problematic) -> Any: ...
    def visit_raw(self, node: raw) -> Any: ...
    def visit_reference(self, node: reference) -> Any: ...
    def visit_revision(self, node: revision) -> Any: ...
    def visit_row(self, node: row) -> Any: ...
    def visit_rubric(self, node: rubric) -> Any: ...
    def visit_section(self, node: section) -> Any: ...
    def visit_sidebar(self, node: sidebar) -> Any: ...
    def visit_status(self, node: status) -> Any: ...
    def visit_strong(self, node: strong) -> Any: ...
    def visit_subscript(self, node: subscript) -> Any: ...
    def visit_substitution_definition(self, node: substitution_definition) -> Any: ...
    def visit_substitution_reference(self, node: substitution_reference) -> Any: ...
    def visit_subtitle(self, node: subtitle) -> Any: ...
    def visit_superscript(self, node: superscript) -> Any: ...
    def visit_system_message(self, node: system_message) -> Any: ...
    def visit_table(self, node: table) -> Any: ...
    def visit_target(self, node: target) -> Any: ...
    def visit_tbody(self, node: tbody) -> Any: ...
    def visit_term(self, node: term) -> Any: ...
    def visit_tgroup(self, node: tgroup) -> Any: ...
    def visit_thead(self, node: thead) -> Any: ...
    def visit_tip(self, node: tip) -> Any: ...
    def visit_title(self, node: title) -> Any: ...
    def visit_title_reference(self, node: title_reference) -> Any: ...
    def visit_topic(self, node: topic) -> Any: ...
    def visit_transition(self, node: transition) -> Any: ...
    def visit_version(self, node: version) -> Any: ...
    def visit_warning(self, node: warning) -> Any: ...
    def depart_Text(self, node: Text) -> Any: ...
    def depart_abbreviation(self, node: abbreviation) -> Any: ...
    def depart_acronym(self, node: acronym) -> Any: ...
    def depart_address(self, node: address) -> Any: ...
    def depart_admonition(self, node: admonition) -> Any: ...
    def depart_attention(self, node: attention) -> Any: ...
    def depart_attribution(self, node: attribution) -> Any: ...
    def depart_author(self, node: author) -> Any: ...
    def depart_authors(self, node: authors) -> Any: ...
    def depart_block_quote(self, node: block_quote) -> Any: ...
    def depart_bullet_list(self, node: bullet_list) -> Any: ...
    def depart_caption(self, node: caption) -> Any: ...
    def depart_caution(self, node: caution) -> Any: ...
    def depart_citation(self, node: citation) -> Any: ...
    def depart_citation_reference(self, node: citation_reference) -> Any: ...
    def depart_classifier(self, node: classifier) -> Any: ...
    def depart_colspec(self, node: colspec) -> Any: ...
    def depart_comment(self, node: comment) -> Any: ...
    def depart_compound(self, node: compound) -> Any: ...
    def depart_contact(self, node: contact) -> Any: ...
    def depart_container(self, node: container) -> Any: ...
    def depart_copyright(self, node: copyright) -> Any: ...
    def depart_danger(self, node: danger) -> Any: ...
    def depart_date(self, node: date) -> Any: ...
    def depart_decoration(self, node: decoration) -> Any: ...
    def depart_definition(self, node: definition) -> Any: ...
    def depart_definition_list(self, node: definition_list) -> Any: ...
    def depart_definition_list_item(self, node: definition_list_item) -> Any: ...
    def depart_description(self, node: description) -> Any: ...
    def depart_docinfo(self, node: docinfo) -> Any: ...
    def depart_doctest_block(self, node: doctest_block) -> Any: ...
    def depart_document(self, node: _Document) -> Any: ...
    def depart_emphasis(self, node: emphasis) -> Any: ...
    def depart_entry(self, node: entry) -> Any: ...
    def depart_enumerated_list(self, node: enumerated_list) -> Any: ...
    def depart_error(self, node: error) -> Any: ...
    def depart_field(self, node: field) -> Any: ...
    def depart_field_body(self, node: field_body) -> Any: ...
    def depart_field_list(self, node: field_list) -> Any: ...
    def depart_field_name(self, node: field_name) -> Any: ...
    def depart_figure(self, node: figure) -> Any: ...
    def depart_footer(self, node: footer) -> Any: ...
    def depart_footnote(self, node: footnote) -> Any: ...
    def depart_footnote_reference(self, node: footnote_reference) -> Any: ...
    def depart_generated(self, node: generated) -> Any: ...
    def depart_header(self, node: header) -> Any: ...
    def depart_hint(self, node: hint) -> Any: ...
    def depart_image(self, node: image) -> Any: ...
    def depart_important(self, node: important) -> Any: ...
    def depart_inline(self, node: inline) -> Any: ...
    def depart_label(self, node: label) -> Any: ...
    def depart_legend(self, node: legend) -> Any: ...
    def depart_line(self, node: line) -> Any: ...
    def depart_line_block(self, node: line_block) -> Any: ...
    def depart_list_item(self, node: list_item) -> Any: ...
    def depart_literal(self, node: literal) -> Any: ...
    def depart_literal_block(self, node: literal_block) -> Any: ...
    def depart_math(self, node: math) -> Any: ...
    def depart_math_block(self, node: math_block) -> Any: ...
    def depart_meta(self, node: meta) -> Any: ...
    def depart_note(self, node: note) -> Any: ...
    def depart_option(self, node: option) -> Any: ...
    def depart_option_argument(self, node: option_argument) -> Any: ...
    def depart_option_group(self, node: option_group) -> Any: ...
    def depart_option_list(self, node: option_list) -> Any: ...
    def depart_option_list_item(self, node: option_list_item) -> Any: ...
    def depart_option_string(self, node: option_string) -> Any: ...
    def depart_organization(self, node: organization) -> Any: ...
    def depart_paragraph(self, node: paragraph) -> Any: ...
    def depart_pending(self, node: pending) -> Any: ...
    def depart_problematic(self, node: problematic) -> Any: ...
    def depart_raw(self, node: raw) -> Any: ...
    def depart_reference(self, node: reference) -> Any: ...
    def depart_revision(self, node: revision) -> Any: ...
    def depart_row(self, node: row) -> Any: ...
    def depart_rubric(self, node: rubric) -> Any: ...
    def depart_section(self, node: section) -> Any: ...
    def depart_sidebar(self, node: sidebar) -> Any: ...
    def depart_status(self, node: status) -> Any: ...
    def depart_strong(self, node: strong) -> Any: ...
    def depart_subscript(self, node: subscript) -> Any: ...
    def depart_substitution_definition(self, node: substitution_definition) -> Any: ...
    def depart_substitution_reference(self, node: substitution_reference) -> Any: ...
    def depart_subtitle(self, node: subtitle) -> Any: ...
    def depart_superscript(self, node: superscript) -> Any: ...
    def depart_system_message(self, node: system_message) -> Any: ...
    def depart_table(self, node: table) -> Any: ...
    def depart_target(self, node: target) -> Any: ...
    def depart_tbody(self, node: tbody) -> Any: ...
    def depart_term(self, node: term) -> Any: ...
    def depart_tgroup(self, node: tgroup) -> Any: ...
    def depart_thead(self, node: thead) -> Any: ...
    def depart_tip(self, node: tip) -> Any: ...
    def depart_title(self, node: title) -> Any: ...
    def depart_title_reference(self, node: title_reference) -> Any: ...
    def depart_topic(self, node: topic) -> Any: ...
    def depart_transition(self, node: transition) -> Any: ...
    def depart_version(self, node: version) -> Any: ...
    def depart_warning(self, node: warning) -> Any: ...

class SparseNodeVisitor(NodeVisitor):
    """
    Base class for sparse traversals, where only certain node types are of
    interest.  When ``visit_...`` & ``depart_...`` methods should be
    implemented for *all* node types (such as for `docutils.writers.Writer`
    subclasses), subclass `NodeVisitor` instead.
    """

class GenericNodeVisitor(NodeVisitor):
    """
    Generic "Visitor" abstract superclass, for simple traversals.

    Unless overridden, each ``visit_...`` method calls `default_visit()`, and
    each ``depart_...`` method (when using `Node.walkabout()`) calls
    `default_departure()`. `default_visit()` (and `default_departure()`) must
    be overridden in subclasses.

    Define fully generic visitors by overriding `default_visit()` (and
    `default_departure()`) only. Define semi-generic visitors by overriding
    individual ``visit_...()`` (and ``depart_...()``) methods also.

    `NodeVisitor.unknown_visit()` (`NodeVisitor.unknown_departure()`) should
    be overridden for default behavior.
    """

    def default_visit(self, node: Node) -> None:
        """Override for generic, uniform traversals."""

    def default_departure(self, node: Node) -> None:
        """Override for generic, uniform traversals."""

class TreeCopyVisitor(GenericNodeVisitor):
    """
    Make a complete copy of a tree or branch, including element attributes.
    """

    parent_stack: list[Node]
    parent: list[Node]
    def get_tree_copy(self) -> Node: ...

class TreePruningException(Exception):
    """
    Base class for `NodeVisitor`-related tree pruning exceptions.

    Raise subclasses from within ``visit_...`` or ``depart_...`` methods
    called from `Node.walk()` and `Node.walkabout()` tree traversals to prune
    the tree traversed.
    """

class SkipChildren(TreePruningException):
    """
    Do not visit any children of the current node.  The current node's
    siblings and ``depart_...`` method are not affected.
    """

class SkipSiblings(TreePruningException):
    """
    Do not visit any more siblings (to the right) of the current node.  The
    current node's children and its ``depart_...`` method are not affected.
    """

class SkipNode(TreePruningException):
    """
    Do not visit the current node's children, and do not call the current
    node's ``depart_...`` method.
    """

class SkipDeparture(TreePruningException):
    """
    Do not call the current node's ``depart_...`` method.  The current node's
    children and siblings are not affected.
    """

class NodeFound(TreePruningException):
    """
    Raise to indicate that the target of a search has been found.  This
    exception must be caught by the client; it is not caught by the traversal
    code.
    """

class StopTraversal(TreePruningException):
    """
    Stop the traversal altogether.  The current node's ``depart_...`` method
    is not affected.  The parent nodes ``depart_...`` methods are also called
    as usual.  No other nodes are visited.  This is an alternative to
    NodeFound that does not cause exception handling to trickle up to the
    caller.
    """

def make_id(string: str) -> str:
    """
    Convert `string` into an identifier and return it.

    Docutils identifiers will conform to the regular expression
    ``[a-z](-?[a-z0-9]+)*``.  For CSS compatibility, identifiers (the "class"
    and "id" attributes) should have no underscores, colons, or periods.
    Hyphens may be used.

    - The `HTML 4.01 spec`_ defines identifiers based on SGML tokens:

          ID and NAME tokens must begin with a letter ([A-Za-z]) and may be
          followed by any number of letters, digits ([0-9]), hyphens ("-"),
          underscores ("_"), colons (":"), and periods (".").

    - However the `CSS1 spec`_ defines identifiers based on the "name" token,
      a tighter interpretation ("flex" tokenizer notation; "latin1" and
      "escape" 8-bit characters have been replaced with entities)::

          unicode     \\[0-9a-f]{1,4}
          latin1      [&iexcl;-&yuml;]
          escape      {unicode}|\\[ -~&iexcl;-&yuml;]
          nmchar      [-a-z0-9]|{latin1}|{escape}
          name        {nmchar}+

    The CSS1 "nmchar" rule does not include underscores ("_"), colons (":"),
    or periods ("."), therefore "class" and "id" attributes should not contain
    these characters. They should be replaced with hyphens ("-"). Combined
    with HTML's requirements (the first character must be a letter; no
    "unicode", "latin1", or "escape" characters), this results in the
    ``[a-z](-?[a-z0-9]+)*`` pattern.

    .. _HTML 4.01 spec: https://www.w3.org/TR/html401
    .. _CSS1 spec: https://www.w3.org/TR/REC-CSS1
    """

def dupname(node: Node, name: str) -> None: ...
def fully_normalize_name(name: str) -> str:
    """Return a case- and whitespace-normalized name."""

def whitespace_normalize_name(name: str) -> str:
    """Return a whitespace-normalized name."""

def serial_escape(value: str) -> str:
    """Escape string values that are elements of a list, for serialization."""

def pseudo_quoteattr(value: str) -> str:
    """Quote attributes for pseudo-xml"""
