from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ["NamedValues"]

class NamedValues:
    """Create named values object.

    The |NamedValues| object represents a collection of string names
    associated with numeric IDs. These objects are used for giving
    names to otherwise numerical values.

    |NamedValues| objects are immutable and duck-type Python
    :class:`dict` object mapping ID to name and vice-versa.

    Parameters
    ----------
    *args: variable number of two-element :py:class:`tuple`

        name: :py:class:`str`
            Value label

        value: :py:class:`int`
            Numeric value

    Keyword Args
    ------------
    name: :py:class:`str`
        Value label

    value: :py:class:`int`
        Numeric value

    Examples
    --------

    .. code-block:: pycon

        >>> nv = NamedValues('a', 'b', ('c', 0), d=1)
        >>> nv
        >>> {'c': 0, 'd': 1, 'a': 2, 'b': 3}
        >>> nv[0]
        'c'
        >>> nv['a']
        2
    """

    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __hash__(self): ...
    def __getitem__(self, key): ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> bool: ...
    def __iter__(self): ...
    def values(self): ...
    def keys(self): ...
    def items(self) -> Generator[Incomplete, None, None]: ...
    def __add__(self, namedValues): ...
    def clone(self, *args, **kwargs): ...
    def getName(self, value): ...
    def getValue(self, name): ...
    def getValues(self, *names): ...
