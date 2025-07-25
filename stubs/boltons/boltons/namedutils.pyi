"""The ``namedutils`` module defines two lightweight container types:
:class:`namedtuple` and :class:`namedlist`. Both are subtypes of built-in
sequence types, which are very fast and efficient. They simply add
named attribute accessors for specific indexes within themselves.

The :class:`namedtuple` is identical to the built-in
:class:`collections.namedtuple`, with a couple of enhancements,
including a ``__repr__`` more suitable to inheritance.

The :class:`namedlist` is the mutable counterpart to the
:class:`namedtuple`, and is much faster and lighter-weight than
full-blown :class:`object`. Consider this if you're implementing nodes
in a tree, graph, or other mutable data structure. If you want an even
skinnier approach, you'll probably have to look to C.
"""

from collections.abc import Iterable

def namedtuple(typename: str, field_names: str | Iterable[str], verbose: bool = False, rename: bool = False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with pos args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessible by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    """

def namedlist(typename: str, field_names: str | Iterable[str], verbose: bool = False, rename: bool = False):
    """Returns a new subclass of list with named fields.

    >>> Point = namedlist('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with pos args or keywords
    >>> p[0] + p[1]                     # indexable like a plain list
    33
    >>> x, y = p                        # unpack like a regular list
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessible by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    """

__all__ = ["namedlist", "namedtuple"]
