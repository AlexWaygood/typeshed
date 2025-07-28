"""Python has a very powerful mapping type at its core: the :class:`dict`
type. While versatile and featureful, the :class:`dict` prioritizes
simplicity and performance. As a result, it does not retain the order
of item insertion [1]_, nor does it store multiple values per key. It
is a fast, unordered 1:1 mapping.

The :class:`OrderedMultiDict` contrasts to the built-in :class:`dict`,
as a relatively maximalist, ordered 1:n subtype of
:class:`dict`. Virtually every feature of :class:`dict` has been
retooled to be intuitive in the face of this added
complexity. Additional methods have been added, such as
:class:`collections.Counter`-like functionality.

A prime advantage of the :class:`OrderedMultiDict` (OMD) is its
non-destructive nature. Data can be added to an :class:`OMD` without being
rearranged or overwritten. The property can allow the developer to
work more freely with the data, as well as make more assumptions about
where input data will end up in the output, all without any extra
work.

One great example of this is the :meth:`OMD.inverted()` method, which
returns a new OMD with the values as keys and the keys as values. All
the data and the respective order is still represented in the inverted
form, all from an operation which would be outright wrong and reckless
with a built-in :class:`dict` or :class:`collections.OrderedDict`.

The OMD has been performance tuned to be suitable for a wide range of
usages, including as a basic unordered MultiDict. Special
thanks to `Mark Williams`_ for all his help.

.. [1] As of 2015, `basic dicts on PyPy are ordered
   <http://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html>`_,
   and as of December 2017, `basic dicts in CPython 3 are now ordered
   <https://mail.python.org/pipermail/python-dev/2017-December/151283.html>`_, as
   well.
.. _Mark Williams: https://github.com/markrwilliams

"""

from _typeshed import SupportsKeysAndGetItem
from collections.abc import Generator, ItemsView, Iterable, KeysView, ValuesView
from typing import NoReturn, TypeVar, overload
from typing_extensions import Self, TypeAlias

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")

class OrderedMultiDict(dict[_KT, _VT]):
    """A MultiDict is a dictionary that can have multiple values per key
    and the OrderedMultiDict (OMD) is a MultiDict that retains
    original insertion order. Common use cases include:

      * handling query strings parsed from URLs
      * inverting a dictionary to create a reverse index (values to keys)
      * stacking data from multiple dictionaries in a non-destructive way

    The OrderedMultiDict constructor is identical to the built-in
    :class:`dict`, and overall the API constitutes an intuitive
    superset of the built-in type:

    >>> omd = OrderedMultiDict()
    >>> omd['a'] = 1
    >>> omd['b'] = 2
    >>> omd.add('a', 3)
    >>> omd.get('a')
    3
    >>> omd.getlist('a')
    [1, 3]

    Some non-:class:`dict`-like behaviors also make an appearance,
    such as support for :func:`reversed`:

    >>> list(reversed(omd))
    ['b', 'a']

    Note that unlike some other MultiDicts, this OMD gives precedence
    to the most recent value added. ``omd['a']`` refers to ``3``, not
    ``1``.

    >>> omd
    OrderedMultiDict([('a', 1), ('b', 2), ('a', 3)])
    >>> omd.poplast('a')
    3
    >>> omd
    OrderedMultiDict([('a', 1), ('b', 2)])
    >>> omd.pop('a')
    1
    >>> omd
    OrderedMultiDict([('b', 2)])

    If you want a safe-to-modify or flat dictionary, use
    :meth:`OrderedMultiDict.todict()`.

    >>> from pprint import pprint as pp  # preserve printed ordering
    >>> omd = OrderedMultiDict([('a', 1), ('b', 2), ('a', 3)])
    >>> pp(omd.todict())
    {'a': 3, 'b': 2}
    >>> pp(omd.todict(multi=True))
    {'a': [1, 3], 'b': [2]}

    With ``multi=False``, items appear with the keys in to original
    insertion order, alongside the most-recently inserted value for
    that key.

    >>> OrderedMultiDict([('a', 1), ('b', 2), ('a', 3)]).items(multi=False)
    [('a', 3), ('b', 2)]

    .. warning::

       ``dict(omd)`` changed behavior `in Python 3.7
       <https://bugs.python.org/issue34320>`_ due to changes made to
       support the transition from :class:`collections.OrderedDict` to
       the built-in dictionary being ordered. Before 3.7, the result
       would be a new dictionary, with values that were lists, similar
       to ``omd.todict(multi=True)`` (but only shallow-copy; the lists
       were direct references to OMD internal structures). From 3.7
       onward, the values became singular, like
       ``omd.todict(multi=False)``. For reliable cross-version
       behavior, just use :meth:`~OrderedMultiDict.todict()`.

    """

    def add(self, k: _KT, v: _VT) -> None:
        """Add a single value *v* under a key *k*. Existing values under *k*
        are preserved.
        """

    def addlist(self, k: _KT, v: Iterable[_VT]) -> None:
        """Add an iterable of values underneath a specific key, preserving
        any values already under that key.

        >>> omd = OrderedMultiDict([('a', -1)])
        >>> omd.addlist('a', range(3))
        >>> omd
        OrderedMultiDict([('a', -1), ('a', 0), ('a', 1), ('a', 2)])

        Called ``addlist`` for consistency with :meth:`getlist`, but
        tuples and other sequences and iterables work.
        """

    def clear(self) -> None:
        """Empty the dictionary."""

    def copy(self) -> Self:
        """Return a shallow copy of the dictionary."""

    def counts(self) -> Self:
        """Returns a mapping from key to number of values inserted under that
        key. Like :py:class:`collections.Counter`, but returns a new
        :class:`OrderedMultiDict`.
        """

    @classmethod
    def fromkeys(cls, keys: _KT, default: _VT | None = None) -> Self:  # type: ignore[override]
        """Create a dictionary from a list of keys, with all the values
        set to *default*, or ``None`` if *default* is not set.
        """

    @overload  # type: ignore[override]
    def get(self, k: _KT, default: None = None) -> _VT | None:
        """Return the value for key *k* if present in the dictionary, else
        *default*. If *default* is not given, ``None`` is returned.
        This method never raises a :exc:`KeyError`.

        To get all values under a key, use :meth:`OrderedMultiDict.getlist`.
        """

    @overload
    def get(self, k: _KT, default: _VT) -> _VT: ...
    def getlist(self, k: _KT, default: list[_VT] = ...) -> list[_VT]:
        """Get all values for key *k* as a list, if *k* is in the
        dictionary, else *default*. The list returned is a copy and
        can be safely mutated. If *default* is not given, an empty
        :class:`list` is returned.
        """

    def inverted(self) -> Self:
        """Returns a new :class:`OrderedMultiDict` with values and keys
        swapped, like creating dictionary transposition or reverse
        index.  Insertion order is retained and all keys and values
        are represented in the output.

        >>> omd = OMD([(0, 2), (1, 2)])
        >>> omd.inverted().getlist(2)
        [0, 1]

        Inverting twice yields a copy of the original:

        >>> omd.inverted().inverted()
        OrderedMultiDict([(0, 2), (1, 2)])
        """

    def items(self, multi: bool = False) -> list[tuple[_KT, _VT]]:  # type: ignore[override]
        """Returns a list containing the output of :meth:`iteritems`.  See
        that method's docs for more details.
        """

    def iteritems(self, multi: bool = False) -> Generator[tuple[_KT, _VT], None, None]:
        """Iterate over the OMD's items in insertion order. By default,
        yields only the most-recently inserted value for each key. Set
        *multi* to ``True`` to get all inserted items.
        """

    def iterkeys(self, multi: bool = False) -> Generator[_KT, None, None]:
        """Iterate over the OMD's keys in insertion order. By default, yields
        each key once, according to the most recent insertion. Set
        *multi* to ``True`` to get all keys, including duplicates, in
        insertion order.
        """

    def itervalues(self, multi: bool = False) -> Generator[_VT, None, None]:
        """Iterate over the OMD's values in insertion order. By default,
        yields the most-recently inserted value per unique key.  Set
        *multi* to ``True`` to get all values according to insertion
        order.
        """

    def keys(self, multi: bool = False) -> list[_KT]:  # type: ignore[override]
        """Returns a list containing the output of :meth:`iterkeys`.  See
        that method's docs for more details.
        """

    def pop(self, k: _KT, default: _VT = ...) -> _VT:  # type: ignore[override]
        """Remove all values under key *k*, returning the most-recently
        inserted value. Raises :exc:`KeyError` if the key is not
        present and no *default* is provided.
        """

    def popall(self, k: _KT, default: _VT = ...) -> list[_VT]:
        """Remove all values under key *k*, returning them in the form of
        a list. Raises :exc:`KeyError` if the key is not present and no
        *default* is provided.
        """

    def poplast(self, k: _KT = ..., default: _VT = ...) -> _VT:
        """Remove and return the most-recently inserted value under the key
        *k*, or the most-recently inserted key if *k* is not
        provided. If no values remain under *k*, it will be removed
        from the OMD.  Raises :exc:`KeyError` if *k* is not present in
        the dictionary, or the dictionary is empty.
        """

    @overload  # type: ignore[override]
    def setdefault(self, k: _KT, default: None = ...) -> _VT | None:
        """If key *k* is in the dictionary, return its value. If not, insert
        *k* with a value of *default* and return *default*. *default*
        defaults to ``None``. See :meth:`dict.setdefault` for more
        information.
        """

    @overload
    def setdefault(self, k: _KT, default: _VT) -> _VT: ...
    def sorted(self, key: _KT | None = None, reverse: bool = False) -> Self:
        """Similar to the built-in :func:`sorted`, except this method returns
        a new :class:`OrderedMultiDict` sorted by the provided key
        function, optionally reversed.

        Args:
            key (callable): A callable to determine the sort key of
              each element. The callable should expect an **item**
              (key-value pair tuple).
            reverse (bool): Set to ``True`` to reverse the ordering.

        >>> omd = OrderedMultiDict(zip(range(3), range(3)))
        >>> omd.sorted(reverse=True)
        OrderedMultiDict([(2, 2), (1, 1), (0, 0)])

        Note that the key function receives an **item** (key-value
        tuple), so the recommended signature looks like:

        >>> omd = OrderedMultiDict(zip('hello', 'world'))
        >>> omd.sorted(key=lambda i: i[1])  # i[0] is the key, i[1] is the val
        OrderedMultiDict([('o', 'd'), ('l', 'l'), ('e', 'o'), ('l', 'r'), ('h', 'w')])
        """

    def sortedvalues(self, key: _KT | None = None, reverse: bool = False) -> Self:
        """Returns a copy of the :class:`OrderedMultiDict` with the same keys
        in the same order as the original OMD, but the values within
        each keyspace have been sorted according to *key* and
        *reverse*.

        Args:
            key (callable): A single-argument callable to determine
              the sort key of each element. The callable should expect
              an **item** (key-value pair tuple).
            reverse (bool): Set to ``True`` to reverse the ordering.

        >>> omd = OrderedMultiDict()
        >>> omd.addlist('even', [6, 2])
        >>> omd.addlist('odd', [1, 5])
        >>> omd.add('even', 4)
        >>> omd.add('odd', 3)
        >>> somd = omd.sortedvalues()
        >>> somd.getlist('even')
        [2, 4, 6]
        >>> somd.keys(multi=True) == omd.keys(multi=True)
        True
        >>> omd == somd
        False
        >>> somd
        OrderedMultiDict([('even', 2), ('even', 4), ('odd', 1), ('odd', 3), ('even', 6), ('odd', 5)])

        As demonstrated above, contents and key order are
        retained. Only value order changes.
        """

    def todict(self, multi: bool = False) -> dict[_KT, _VT]:
        """Gets a basic :class:`dict` of the items in this dictionary. Keys
        are the same as the OMD, values are the most recently inserted
        values for each key.

        Setting the *multi* arg to ``True`` is yields the same
        result as calling :class:`dict` on the OMD, except that all the
        value lists are copies that can be safely mutated.
        """

    def update(self, E: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]], **F) -> None:  # type: ignore[override]
        """Add items from a dictionary or iterable (and/or keyword arguments),
        overwriting values under an existing key. See
        :meth:`dict.update` for more details.
        """

    def update_extend(self, E: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]], **F) -> None:
        """Add items from a dictionary, iterable, and/or keyword
        arguments without overwriting existing items present in the
        dictionary. Like :meth:`update`, but adds to existing keys
        instead of overwriting them.
        """

    def values(self, multi: bool = False) -> list[_VT]:  # type: ignore[override]
        """Returns a list containing the output of :meth:`itervalues`.  See
        that method's docs for more details.
        """

    def viewitems(self) -> ItemsView[_KT, _VT]:
        """OMD.viewitems() -> a set-like object providing a view on OMD's items"""

    def viewkeys(self) -> KeysView[_KT]:
        """OMD.viewkeys() -> a set-like object providing a view on OMD's keys"""

    def viewvalues(self) -> ValuesView[_VT]:
        """OMD.viewvalues() -> an object providing a view on OMD's values"""

OMD: TypeAlias = OrderedMultiDict[_KT, _VT]
MultiDict: TypeAlias = OrderedMultiDict[_KT, _VT]

class FastIterOrderedMultiDict(OrderedMultiDict[_KT, _VT]):  # undocumented
    """An OrderedMultiDict backed by a skip list.  Iteration over keys
    is faster and uses constant memory but adding duplicate key-value
    pairs is slower. Brainchild of Mark Williams.
    """

    def iteritems(self, multi: bool = False) -> Generator[tuple[_KT, _VT], None, None]: ...
    def iterkeys(self, multi: bool = False) -> Generator[_KT, None, None]: ...

class OneToOne(dict[_KT, _VT]):
    """Implements a one-to-one mapping dictionary. In addition to
    inheriting from and behaving exactly like the builtin
    :class:`dict`, all values are automatically added as keys on a
    reverse mapping, available as the `inv` attribute. This
    arrangement keeps key and value namespaces distinct.

    Basic operations are intuitive:

    >>> oto = OneToOne({'a': 1, 'b': 2})
    >>> print(oto['a'])
    1
    >>> print(oto.inv[1])
    a
    >>> len(oto)
    2

    Overwrites happens in both directions:

    >>> oto.inv[1] = 'c'
    >>> print(oto.get('a'))
    None
    >>> len(oto)
    2

    For a very similar project, with even more one-to-one
    functionality, check out `bidict <https://github.com/jab/bidict>`_.
    """

    inv: OneToOne[_VT, _KT]
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    def pop(self, key: _KT, default: _VT | _T = ...) -> _VT | _T: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    def setdefault(self, key: _KT, default: _VT | None = None) -> _VT: ...
    @classmethod
    def unique(cls, *a, **kw) -> Self:
        """This alternate constructor for OneToOne will raise an exception
        when input values overlap. For instance:

        >>> OneToOne.unique({'a': 1, 'b': 1})
        Traceback (most recent call last):
        ...
        ValueError: expected unique values, got multiple keys for the following values: ...

        This even works across inputs:

        >>> a_dict = {'a': 2}
        >>> OneToOne.unique(a_dict, b=2)
        Traceback (most recent call last):
        ...
        ValueError: expected unique values, got multiple keys for the following values: ...
        """

    def update(self, dict_or_iterable, **kw) -> None: ...  # type: ignore[override]

class ManyToMany(dict[_KT, frozenset[_VT]]):
    """
    a dict-like entity that represents a many-to-many relationship
    between two groups of objects

    behaves like a dict-of-tuples; also has .inv which is kept
    up to date which is a dict-of-tuples in the other direction

    also, can be used as a directed graph among hashable python objects
    """

    data: dict[_KT, set[_VT]]
    inv: dict[_VT, set[_KT]]
    # def __contains__(self, key: _KT): ...
    def __delitem__(self, key: _KT) -> None: ...
    def __eq__(self, other): ...
    def __getitem__(self, key: _KT): ...
    def __init__(
        self, items: ManyToMany[_KT, _VT] | SupportsKeysAndGetItem[_KT, _VT] | tuple[_KT, _VT] | None = None
    ) -> None: ...
    def __iter__(self): ...
    def __len__(self): ...
    def __setitem__(self, key: _KT, vals: Iterable[_VT]) -> None: ...
    def add(self, key: _KT, val: _VT) -> None: ...
    def get(self, key: _KT, default: frozenset[_VT] = ...) -> frozenset[_VT]: ...  # type: ignore[override]
    def iteritems(self) -> Generator[tuple[_KT, _VT], None, None]: ...
    def keys(self): ...
    def remove(self, key: _KT, val: _VT) -> None: ...
    def replace(self, key: _KT, newkey: _KT) -> None:
        """
        replace instances of key by newkey
        """

    def update(self, iterable: ManyToMany[_KT, _VT] | SupportsKeysAndGetItem[_KT, _VT] | tuple[_KT, _VT]) -> None:  # type: ignore[override]
        """given an iterable of (key, val), add them all"""

def subdict(d: dict[_KT, _VT], keep: Iterable[_KT] | None = None, drop: Iterable[_KT] | None = None) -> dict[_KT, _VT]:
    """Compute the "subdictionary" of a dict, *d*.

    A subdict is to a dict what a subset is a to set. If *A* is a
    subdict of *B*, that means that all keys of *A* are present in
    *B*.

    Returns a new dict with any keys in *drop* removed, and any keys
    in *keep* still present, provided they were in the original
    dict. *keep* defaults to all keys, *drop* defaults to empty, so
    without one of these arguments, calling this function is
    equivalent to calling ``dict()``.

    >>> from pprint import pprint as pp
    >>> pp(subdict({'a': 1, 'b': 2}))
    {'a': 1, 'b': 2}
    >>> subdict({'a': 1, 'b': 2, 'c': 3}, drop=['b', 'c'])
    {'a': 1}
    >>> pp(subdict({'a': 1, 'b': 2, 'c': 3}, keep=['a', 'c']))
    {'a': 1, 'c': 3}

    """

class FrozenHashError(TypeError): ...  # undocumented

class FrozenDict(dict[_KT, _VT]):
    """An immutable dict subtype that is hashable and can itself be used
    as a :class:`dict` key or :class:`set` entry. What
    :class:`frozenset` is to :class:`set`, FrozenDict is to
    :class:`dict`.

    There was once an attempt to introduce such a type to the standard
    library, but it was rejected: `PEP 416 <https://www.python.org/dev/peps/pep-0416/>`_.

    Because FrozenDict is a :class:`dict` subtype, it automatically
    works everywhere a dict would, including JSON serialization.

    """

    def __copy__(self) -> Self: ...
    @classmethod
    def fromkeys(cls, keys: Iterable[_KT], value: _VT | None = None) -> Self: ...  # type: ignore[override]
    def updated(self, *a, **kw) -> Self:
        """Make a copy and add items from a dictionary or iterable (and/or
        keyword arguments), overwriting values under an existing
        key. See :meth:`dict.update` for more details.
        """

    def __ior__(self, *a, **kw) -> NoReturn:  # type: ignore[misc] # noqa: Y034 # Signature conflicts with superclass
        """raises a TypeError, because FrozenDicts are immutable"""

    def __setitem__(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def __delitem__(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def update(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def pop(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def popitem(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def setdefault(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

    def clear(self, *a, **kw) -> NoReturn:
        """raises a TypeError, because FrozenDicts are immutable"""

__all__ = ["MultiDict", "OMD", "OrderedMultiDict", "OneToOne", "ManyToMany", "subdict", "FrozenDict"]
