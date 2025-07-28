"""
The :class:`set` type brings the practical expressiveness of
set theory to Python. It has a very rich API overall, but lacks a
couple of fundamental features. For one, sets are not ordered. On top
of this, sets are not indexable, i.e, ``my_set[8]`` will raise an
:exc:`TypeError`. The :class:`IndexedSet` type remedies both of these
issues without compromising on the excellent complexity
characteristics of Python's built-in set implementation.
"""

from collections.abc import Collection, Container, Generator, Iterable, Iterator, MutableSet
from itertools import islice
from typing import Any, Literal, Protocol, SupportsIndex, TypeVar, overload
from typing_extensions import Self

_T_co = TypeVar("_T_co", covariant=True)

class _RSub(Iterable[_T_co], Protocol):
    def __new__(cls: type[_RSub[_T_co]], param: list[_T_co], /) -> _RSub[_T_co]: ...

class IndexedSet(MutableSet[Any]):
    """``IndexedSet`` is a :class:`collections.MutableSet` that maintains
    insertion order and uniqueness of inserted elements. It's a hybrid
    type, mostly like an OrderedSet, but also :class:`list`-like, in
    that it supports indexing and slicing.

    Args:
        other (iterable): An optional iterable used to initialize the set.

    >>> x = IndexedSet(list(range(4)) + list(range(8)))
    >>> x
    IndexedSet([0, 1, 2, 3, 4, 5, 6, 7])
    >>> x - set(range(2))
    IndexedSet([2, 3, 4, 5, 6, 7])
    >>> x[-1]
    7
    >>> fcr = IndexedSet('freecreditreport.com')
    >>> ''.join(fcr[:fcr.index('.')])
    'frecditpo'

    Standard set operators and interoperation with :class:`set` are
    all supported:

    >>> fcr & set('cash4gold.com')
    IndexedSet(['c', 'd', 'o', '.', 'm'])

    As you can see, the ``IndexedSet`` is almost like a ``UniqueList``,
    retaining only one copy of a given value, in the order it was
    first added. For the curious, the reason why IndexedSet does not
    support setting items based on index (i.e, ``__setitem__()``),
    consider the following dilemma::

      my_indexed_set = [A, B, C, D]
      my_indexed_set[2] = A

    At this point, a set requires only one *A*, but a :class:`list` would
    overwrite *C*. Overwriting *C* would change the length of the list,
    meaning that ``my_indexed_set[2]`` would not be *A*, as expected with a
    list, but rather *D*. So, no ``__setitem__()``.

    Otherwise, the API strives to be as complete a union of the
    :class:`list` and :class:`set` APIs as possible.
    """

    item_index_map: dict[Any, Any]
    item_list: list[Any]
    dead_indices: list[int]
    def __init__(self, other: Iterable[Any] | None = None) -> None: ...
    def __len__(self) -> int: ...
    def __contains__(self, item: Any) -> bool: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __reversed__(self) -> Generator[Any, None, None]: ...
    @classmethod
    def from_iterable(cls, it: Iterable[Any]) -> Self:
        """from_iterable(it) -> create a set from an iterable"""

    def add(self, item: Any) -> None:
        """add(item) -> add item to the set"""

    def remove(self, item: Any) -> None:
        """remove(item) -> remove item from the set, raises if not present"""

    def discard(self, item: Any) -> None:
        """discard(item) -> discard item from the set (does not raise)"""

    def clear(self) -> None:
        """clear() -> empty the set"""

    def isdisjoint(self, other: Iterable[Any]) -> bool:
        """isdisjoint(other) -> return True if no overlap with other"""

    def issubset(self, other: Collection[Any]) -> bool:
        """issubset(other) -> return True if other contains this set"""

    def issuperset(self, other: Collection[Any]) -> bool:
        """issuperset(other) -> return True if set contains other"""

    def union(self, *others: Iterable[Any]) -> Self:
        """union(*others) -> return a new set containing this set and others"""

    def iter_intersection(self, *others: Container[Any]) -> Generator[Any, None, None]:
        """iter_intersection(*others) -> iterate over elements also in others"""

    def intersection(self, *others: Container[Any]) -> Self:
        """intersection(*others) -> get a set with overlap of this and others"""

    def iter_difference(self, *others: Iterable[Any]) -> Generator[Any, None, None]:
        """iter_difference(*others) -> iterate over elements not in others"""

    def difference(self, *others: Iterable[Any]) -> Self:
        """difference(*others) -> get a new set with elements not in others"""

    def symmetric_difference(self, *others: Container[Any]) -> Self:
        """symmetric_difference(*others) -> XOR set of this and others"""
    # __or__ = union
    __ror__ = union
    # __and__ = intersection
    __rand__ = intersection
    # __sub__ = difference
    # __xor__ = symmetric_difference
    __rxor__ = symmetric_difference
    def __rsub__(self, other: _RSub[_T_co]) -> _RSub[_T_co]: ...
    def update(self, *others: Iterable[Any]) -> None:
        """update(*others) -> add values from one or more iterables"""

    def intersection_update(self, *others: Iterable[Any]) -> None:
        """intersection_update(*others) -> discard self.difference(*others)"""

    def difference_update(self, *others: Container[Any]) -> None:
        """difference_update(*others) -> discard self.intersection(*others)"""

    def symmetric_difference_update(self, other: Iterable[Any]) -> None:
        """symmetric_difference_update(other) -> in-place XOR with other"""

    def iter_slice(self, start: int, stop: int, step: int | None = None) -> islice[Iterable[Any]]:
        """iterate over a slice of the set"""

    @overload
    def __getitem__(self, index: slice) -> Self: ...
    @overload
    def __getitem__(self, index: SupportsIndex) -> Any: ...
    def pop(self, index: int | None = None) -> Any:
        """pop(index) -> remove the item at a given index (-1 by default)"""

    def count(self, val: Any) -> Literal[0, 1]:
        """count(val) -> count number of instances of value (0 or 1)"""

    def reverse(self) -> None:
        """reverse() -> reverse the contents of the set in-place"""

    def sort(self, **kwargs) -> None:
        """sort() -> sort the contents of the set in-place"""

    def index(self, val: Any) -> int:
        """index(val) -> get the index of a value, raises if not present"""

def complement(wrapped: Iterable[Any]) -> _ComplementSet:
    """Given a :class:`set`, convert it to a **complement set**.

    Whereas a :class:`set` keeps track of what it contains, a
    `complement set
    <https://en.wikipedia.org/wiki/Complement_(set_theory)>`_ keeps
    track of what it does *not* contain. For example, look what
    happens when we intersect a normal set with a complement set::

    >>> list(set(range(5)) & complement(set([2, 3])))
    [0, 1, 4]

    We get the everything in the left that wasn't in the right,
    because intersecting with a complement is the same as subtracting
    a normal set.

    Args:
        wrapped (set): A set or any other iterable which should be
           turned into a complement set.

    All set methods and operators are supported by complement sets,
    between other :func:`complement`-wrapped sets and/or regular
    :class:`set` objects.

    Because a complement set only tracks what elements are *not* in
    the set, functionality based on set contents is unavailable:
    :func:`len`, :func:`iter` (and for loops), and ``.pop()``. But a
    complement set can always be turned back into a regular set by
    complementing it again:

    >>> s = set(range(5))
    >>> complement(complement(s)) == s
    True

    .. note::

       An empty complement set corresponds to the concept of a
       `universal set <https://en.wikipedia.org/wiki/Universal_set>`_
       from mathematics.

    Complement sets by example
    ^^^^^^^^^^^^^^^^^^^^^^^^^^

    Many uses of sets can be expressed more simply by using a
    complement. Rather than trying to work out in your head the proper
    way to invert an expression, you can just throw a complement on
    the set. Consider this example of a name filter::

        >>> class NamesFilter(object):
        ...    def __init__(self, allowed):
        ...        self._allowed = allowed
        ...
        ...    def filter(self, names):
        ...        return [name for name in names if name in self._allowed]
        >>> NamesFilter(set(['alice', 'bob'])).filter(['alice', 'bob', 'carol'])
        ['alice', 'bob']

    What if we want to just express "let all the names through"?

    We could try to enumerate all of the expected names::

       ``NamesFilter({'alice', 'bob', 'carol'})``

    But this is very brittle -- what if at some point over this
    object is changed to filter ``['alice', 'bob', 'carol', 'dan']``?

    Even worse, what about the poor programmer who next works
    on this piece of code?  They cannot tell whether the purpose
    of the large allowed set was "allow everything", or if 'dan'
    was excluded for some subtle reason.

    A complement set lets the programmer intention be expressed
    succinctly and directly::

       NamesFilter(complement(set()))

    Not only is this code short and robust, it is easy to understand
    the intention.

    """

class _ComplementSet:
    """
    helper class for complement() that implements the set methods
    """

    def __init__(
        self, included: set[Any] | frozenset[Any] | None = None, excluded: set[Any] | frozenset[Any] | None = None
    ) -> None: ...
    def complemented(self) -> _ComplementSet:
        """return a complement of the current set"""
    __invert__ = complemented
    def complement(self) -> None:
        """convert the current set to its complement in-place"""

    def __contains__(self, item: Any) -> bool: ...
    def add(self, item: Any) -> None: ...
    def remove(self, item: Any) -> None: ...
    def pop(self) -> Any: ...
    def intersection(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def __and__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    __rand__ = __and__
    def __iand__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> Self: ...
    def union(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def __or__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    __ror__ = __or__
    def __ior__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> Self: ...
    def update(self, items: Iterable[Any]) -> None: ...
    def discard(self, items: Iterable[Any]) -> None: ...
    def symmetric_difference(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def __xor__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    __rxor__ = __xor__
    def symmetric_difference_update(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> None: ...
    def isdisjoint(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool: ...
    def issubset(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool:
        """everything missing from other is also missing from self"""

    def __le__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool: ...
    def __lt__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool: ...
    def issuperset(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool:
        """everything missing from self is also missing from super"""

    def __ge__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool: ...
    def __gt__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> bool: ...
    def difference(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def __sub__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def __rsub__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> _ComplementSet: ...
    def difference_update(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> None: ...
    def __isub__(self, other: set[Any] | frozenset[Any] | _ComplementSet) -> Self: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __bool__(self) -> bool: ...

__all__ = ["IndexedSet", "complement"]
