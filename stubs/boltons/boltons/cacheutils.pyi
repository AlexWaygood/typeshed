"""``cacheutils`` contains consistent implementations of fundamental
cache types. Currently there are two to choose from:

  * :class:`LRI` - Least-recently inserted
  * :class:`LRU` - Least-recently used

Both caches are :class:`dict` subtypes, designed to be as
interchangeable as possible, to facilitate experimentation. A key
practice with performance enhancement with caching is ensuring that
the caching strategy is working. If the cache is constantly missing,
it is just adding more overhead and code complexity. The standard
statistics are:

  * ``hit_count`` - the number of times the queried key has been in
    the cache
  * ``miss_count`` - the number of times a key has been absent and/or
    fetched by the cache
  * ``soft_miss_count`` - the number of times a key has been absent,
    but a default has been provided by the caller, as with
    :meth:`dict.get` and :meth:`dict.setdefault`. Soft misses are a
    subset of misses, so this number is always less than or equal to
    ``miss_count``.

Additionally, ``cacheutils`` provides :class:`ThresholdCounter`, a
cache-like bounded counter useful for online statistics collection.

Learn more about `caching algorithms on Wikipedia
<https://en.wikipedia.org/wiki/Cache_algorithms#Examples>`_.

"""

import weakref
from _typeshed import Incomplete, SupportsItems, SupportsKeysAndGetItem
from collections.abc import Callable, Generator, Hashable, Iterable, Iterator, Mapping
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Self

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")

PREV: int
NEXT: int
KEY: int
VALUE: int
DEFAULT_MAX_SIZE: int

class LRI(dict[_KT, _VT]):
    """The ``LRI`` implements the basic *Least Recently Inserted* strategy to
    caching. One could also think of this as a ``SizeLimitedDefaultDict``.

    *on_miss* is a callable that accepts the missing key (as opposed
    to :class:`collections.defaultdict`'s "default_factory", which
    accepts no arguments.) Also note that, like the :class:`LRI`,
    the ``LRI`` is instrumented with statistics tracking.

    >>> cap_cache = LRI(max_size=2)
    >>> cap_cache['a'], cap_cache['b'] = 'A', 'B'
    >>> from pprint import pprint as pp
    >>> pp(dict(cap_cache))
    {'a': 'A', 'b': 'B'}
    >>> [cap_cache['b'] for i in range(3)][0]
    'B'
    >>> cap_cache['c'] = 'C'
    >>> print(cap_cache.get('a'))
    None
    >>> cap_cache.hit_count, cap_cache.miss_count, cap_cache.soft_miss_count
    (3, 1, 1)
    """

    hit_count: int
    miss_count: int
    soft_miss_count: int
    max_size: int
    on_miss: Callable[[_KT], _VT] | None
    def __init__(self, max_size: int = 128, values=None, on_miss: Callable[[_KT], _VT] | None = None) -> None: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    @overload
    def get(self, key: _KT, default: None = None) -> _VT | None: ...
    @overload
    def get(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def get(self, key: _KT, default: _T) -> _T | _VT: ...
    def __delitem__(self, key: _KT) -> None: ...
    @overload
    def pop(self, key: _KT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T) -> _T | _VT: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    @overload
    def setdefault(self, key: _KT, default: None = None) -> _VT | None: ...
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    def update(self, E: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]], **F: _VT) -> None: ...  # type: ignore[override]

class LRU(LRI[_KT, _VT]):
    """The ``LRU`` is :class:`dict` subtype implementation of the
    *Least-Recently Used* caching strategy.

    Args:
        max_size (int): Max number of items to cache. Defaults to ``128``.
        values (iterable): Initial values for the cache. Defaults to ``None``.
        on_miss (callable): a callable which accepts a single argument, the
            key not present in the cache, and returns the value to be cached.

    >>> cap_cache = LRU(max_size=2)
    >>> cap_cache['a'], cap_cache['b'] = 'A', 'B'
    >>> from pprint import pprint as pp
    >>> pp(dict(cap_cache))
    {'a': 'A', 'b': 'B'}
    >>> [cap_cache['b'] for i in range(3)][0]
    'B'
    >>> cap_cache['c'] = 'C'
    >>> print(cap_cache.get('a'))
    None

    This cache is also instrumented with statistics
    collection. ``hit_count``, ``miss_count``, and ``soft_miss_count``
    are all integer members that can be used to introspect the
    performance of the cache. ("Soft" misses are misses that did not
    raise :exc:`KeyError`, e.g., ``LRU.get()`` or ``on_miss`` was used to
    cache a default.

    >>> cap_cache.hit_count, cap_cache.miss_count, cap_cache.soft_miss_count
    (3, 1, 1)

    Other than the size-limiting caching behavior and statistics,
    ``LRU`` acts like its parent class, the built-in Python :class:`dict`.
    """

    def __getitem__(self, key: _KT) -> _VT: ...

def make_cache_key(
    args: Iterable[Hashable],
    kwargs: SupportsItems[Hashable, Hashable],
    typed: bool = False,
    kwarg_mark: object = ...,
    fasttypes: frozenset[type] = ...,
):
    """Make a generic key from a function's positional and keyword
    arguments, suitable for use in caches. Arguments within *args* and
    *kwargs* must be `hashable`_. If *typed* is ``True``, ``3`` and
    ``3.0`` will be treated as separate keys.

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    >>> tuple(make_cache_key(('a', 'b'), {'c': ('d')}))
    ('a', 'b', _KWARG_MARK, ('c', 'd'))

    .. _hashable: https://docs.python.org/2/glossary.html#term-hashable
    """

class CachedFunction:
    """This type is used by :func:`cached`, below. Instances of this
    class are used to wrap functions in caching logic.
    """

    func: Incomplete
    get_cache: Incomplete
    scoped: Incomplete
    typed: Incomplete
    key_func: Incomplete
    def __init__(
        self,
        func,
        cache: Mapping[Any, Any] | Callable[..., Incomplete],
        scoped: bool = True,
        typed: bool = False,
        key: Callable[..., Incomplete] | None = None,
    ): ...
    def __call__(self, *args, **kwargs): ...

class CachedMethod:
    """Similar to :class:`CachedFunction`, this type is used by
    :func:`cachedmethod` to wrap methods in caching logic.
    """

    func: Incomplete
    get_cache: Incomplete
    scoped: Incomplete
    typed: Incomplete
    key_func: Incomplete
    bound_to: Incomplete
    def __init__(
        self,
        func,
        cache: Mapping[Any, Any] | Callable[..., Incomplete],
        scoped: bool = True,
        typed: bool = False,
        key: Callable[..., Incomplete] | None = None,
    ): ...
    def __get__(self, obj, objtype=None): ...
    def __call__(self, *args, **kwargs): ...

def cached(
    cache: Mapping[Any, Any] | Callable[..., Incomplete],
    scoped: bool = True,
    typed: bool = False,
    key: Callable[..., Incomplete] | None = None,
):
    """Cache any function with the cache object of your choosing. Note
    that the function wrapped should take only `hashable`_ arguments.

    Args:
        cache (Mapping): Any :class:`dict`-like object suitable for
            use as a cache. Instances of the :class:`LRU` and
            :class:`LRI` are good choices, but a plain :class:`dict`
            can work in some cases, as well. This argument can also be
            a callable which accepts no arguments and returns a mapping.
        scoped (bool): Whether the function itself is part of the
            cache key.  ``True`` by default, different functions will
            not read one another's cache entries, but can evict one
            another's results. ``False`` can be useful for certain
            shared cache use cases. More advanced behavior can be
            produced through the *key* argument.
        typed (bool): Whether to factor argument types into the cache
            check. Default ``False``, setting to ``True`` causes the
            cache keys for ``3`` and ``3.0`` to be considered unequal.

    >>> my_cache = LRU()
    >>> @cached(my_cache)
    ... def cached_lower(x):
    ...     return x.lower()
    ...
    >>> cached_lower("CaChInG's FuN AgAiN!")
    "caching's fun again!"
    >>> len(my_cache)
    1

    .. _hashable: https://docs.python.org/2/glossary.html#term-hashable

    """

def cachedmethod(
    cache: Mapping[Any, Any] | Callable[..., Incomplete],
    scoped: bool = True,
    typed: bool = False,
    key: Callable[..., Incomplete] | None = None,
):
    """Similar to :func:`cached`, ``cachedmethod`` is used to cache
    methods based on their arguments, using any :class:`dict`-like
    *cache* object.

    Args:
        cache (str/Mapping/callable): Can be the name of an attribute
            on the instance, any Mapping/:class:`dict`-like object, or
            a callable which returns a Mapping.
        scoped (bool): Whether the method itself and the object it is
            bound to are part of the cache keys. ``True`` by default,
            different methods will not read one another's cache
            results. ``False`` can be useful for certain shared cache
            use cases. More advanced behavior can be produced through
            the *key* arguments.
        typed (bool): Whether to factor argument types into the cache
            check. Default ``False``, setting to ``True`` causes the
            cache keys for ``3`` and ``3.0`` to be considered unequal.
        key (callable): A callable with a signature that matches
            :func:`make_cache_key` that returns a tuple of hashable
            values to be used as the key in the cache.

    >>> class Lowerer(object):
    ...     def __init__(self):
    ...         self.cache = LRI()
    ...
    ...     @cachedmethod('cache')
    ...     def lower(self, text):
    ...         return text.lower()
    ...
    >>> lowerer = Lowerer()
    >>> lowerer.lower('WOW WHO COULD GUESS CACHING COULD BE SO NEAT')
    'wow who could guess caching could be so neat'
    >>> len(lowerer.cache)
    1

    """

class cachedproperty(Generic[_KT, _VT]):
    """The ``cachedproperty`` is used similar to :class:`property`, except
    that the wrapped method is only called once. This is commonly used
    to implement lazy attributes.

    After the property has been accessed, the value is stored on the
    instance itself, using the same name as the cachedproperty. This
    allows the cache to be cleared with :func:`delattr`, or through
    manipulating the object's ``__dict__``.
    """

    func: Callable[[_KT], _VT]
    def __init__(self, func: Callable[[_KT], _VT]) -> None: ...
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: _KT, objtype: type | None = None) -> _VT: ...

class ThresholdCounter(Generic[_T]):
    """A **bounded** dict-like Mapping from keys to counts. The
    ThresholdCounter automatically compacts after every (1 /
    *threshold*) additions, maintaining exact counts for any keys
    whose count represents at least a *threshold* ratio of the total
    data. In other words, if a particular key is not present in the
    ThresholdCounter, its count represents less than *threshold* of
    the total data.

    >>> tc = ThresholdCounter(threshold=0.1)
    >>> tc.add(1)
    >>> tc.items()
    [(1, 1)]
    >>> tc.update([2] * 10)
    >>> tc.get(1)
    0
    >>> tc.add(5)
    >>> 5 in tc
    True
    >>> len(list(tc.elements()))
    11

    As you can see above, the API is kept similar to
    :class:`collections.Counter`. The most notable feature omissions
    being that counted items cannot be set directly, uncounted, or
    removed, as this would disrupt the math.

    Use the ThresholdCounter when you need best-effort long-lived
    counts for dynamically-keyed data. Without a bounded datastructure
    such as this one, the dynamic keys often represent a memory leak
    and can impact application reliability. The ThresholdCounter's
    item replacement strategy is fully deterministic and can be
    thought of as *Amortized Least Relevant*. The absolute upper bound
    of keys it will store is *(2/threshold)*, but realistically
    *(1/threshold)* is expected for uniformly random datastreams, and
    one or two orders of magnitude better for real-world data.

    This algorithm is an implementation of the Lossy Counting
    algorithm described in "Approximate Frequency Counts over Data
    Streams" by Manku & Motwani. Hat tip to Kurt Rose for discovery
    and initial implementation.

    """

    total: int
    def __init__(self, threshold: float = 0.001) -> None: ...
    @property
    def threshold(self) -> float: ...
    def add(self, key: _T) -> None:
        """Increment the count of *key* by 1, automatically adding it if it
        does not exist.

        Cache compaction is triggered every *1/threshold* additions.
        """

    def elements(self) -> Iterator[_T]:
        """Return an iterator of all the common elements tracked by the
        counter. Yields each key as many times as it has been seen.
        """

    def most_common(self, n: int | None = None) -> list[tuple[_T, int]]:
        """Get the top *n* keys and counts as tuples. If *n* is omitted,
        returns all the pairs.
        """

    def get_common_count(self) -> int:
        """Get the sum of counts for keys exceeding the configured data
        threshold.
        """

    def get_uncommon_count(self) -> int:
        """Get the sum of counts for keys that were culled because the
        associated counts represented less than the configured
        threshold. The long-tail counts.
        """

    def get_commonality(self) -> float:
        """Get a float representation of the effective count accuracy. The
        higher the number, the less uniform the keys being added, and
        the higher accuracy and efficiency of the ThresholdCounter.

        If a stronger measure of data cardinality is required,
        consider using hyperloglog.
        """

    def __getitem__(self, key: _T) -> int: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: _T) -> bool: ...
    def iterkeys(self) -> Iterator[_T]: ...
    def keys(self) -> list[_T]: ...
    def itervalues(self) -> Generator[int, None, None]: ...
    def values(self) -> list[int]: ...
    def iteritems(self) -> Generator[tuple[_T, int], None, None]: ...
    def items(self) -> list[tuple[_T, int]]: ...
    def get(self, key: _T, default: int = 0) -> int:
        """Get count for *key*, defaulting to 0."""

    def update(self, iterable: Iterable[_T] | Mapping[_T, int], **kwargs: Iterable[_T] | Mapping[_T, int]) -> None:
        """Like dict.update() but add counts instead of replacing them, used
        to add multiple items in one call.

        Source can be an iterable of keys to add, or a mapping of keys
        to integer counts.
        """

class MinIDMap(Generic[_T]):
    """
    Assigns arbitrary weakref-able objects the smallest possible unique
    integer IDs, such that no two objects have the same ID at the same
    time.

    Maps arbitrary hashable objects to IDs.

    Based on https://gist.github.com/kurtbrose/25b48114de216a5e55df
    """

    mapping: weakref.WeakKeyDictionary[_T, tuple[int, weakref.ReferenceType[_T]]]
    ref_map: dict[weakref.ReferenceType[_T], int]
    free: list[int]
    def __init__(self) -> None: ...
    def get(self, a: _T) -> int: ...
    def drop(self, a: _T) -> None: ...
    def __contains__(self, a: _T) -> bool: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __len__(self) -> int: ...
    def iteritems(self) -> Iterator[tuple[_T, int]]: ...
