"""The Python Garbage Collector (`GC`_) doesn't usually get too much
attention, probably because:

  - Python's `reference counting`_ effectively handles the vast majority of
    unused objects
  - People are slowly learning to avoid implementing `object.__del__()`_
  - The collection itself strikes a good balance between simplicity and
    power (`tunable generation sizes`_)
  - The collector itself is fast and rarely the cause of long pauses
    associated with GC in other runtimes

Even so, for many applications, the time will come when the developer
will need to track down:

  - Circular references
  - Misbehaving objects (locks, ``__del__()``)
  - Memory leaks
  - Or just ways to shave off a couple percent of execution time

Thanks to the :mod:`gc` module, the GC is a well-instrumented entry
point for exactly these tasks, and ``gcutils`` aims to facilitate it
further.

.. _GC: https://docs.python.org/2/glossary.html#term-garbage-collection
.. _reference counting: https://docs.python.org/2/glossary.html#term-reference-count
.. _object.__del__(): https://docs.python.org/2/glossary.html#term-reference-count
.. _tunable generation sizes: https://docs.python.org/2/library/gc.html#gc.set_threshold
"""

from typing import TypeVar

_T = TypeVar("_T")

def get_all(type_obj: type[_T], include_subtypes: bool = True) -> list[_T]:
    """Get a list containing all instances of a given type.  This will
    work for the vast majority of types out there.

    >>> class Ratking(object): pass
    >>> wiki, hak, sport = Ratking(), Ratking(), Ratking()
    >>> len(get_all(Ratking))
    3

    However, there are some exceptions. For example, ``get_all(bool)``
    returns an empty list because ``True`` and ``False`` are
    themselves built-in and not tracked.

    >>> get_all(bool)
    []

    Still, it's not hard to see how this functionality can be used to
    find all instances of a leaking type and track them down further
    using :func:`gc.get_referrers` and :func:`gc.get_referents`.

    ``get_all()`` is optimized such that getting instances of
    user-created types is quite fast. Setting *include_subtypes* to
    ``False`` will further increase performance in cases where
    instances of subtypes aren't required.

    .. note::

      There are no guarantees about the state of objects returned by
      ``get_all()``, especially in concurrent environments. For
      instance, it is possible for an object to be in the middle of
      executing its ``__init__()`` and be only partially constructed.
    """

class GCToggler:
    """The ``GCToggler`` is a context-manager that allows one to safely
    take more control of your garbage collection schedule. Anecdotal
    experience says certain object-creation-heavy tasks see speedups
    of around 10% by simply doing one explicit collection at the very
    end, especially if most of the objects will stay resident.

    Two GCTogglers are already present in the ``gcutils`` module:

    - :data:`toggle_gc` simply turns off GC at context entrance, and
      re-enables at exit
    - :data:`toggle_gc_postcollect` does the same, but triggers an
      explicit collection after re-enabling.

    >>> with toggle_gc:
    ...     x = [object() for i in range(1000)]

    Between those two instances, the ``GCToggler`` type probably won't
    be used much directly, but is documented for inheritance purposes.
    """

    postcollect: bool
    def __init__(self, postcollect: bool = False) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

toggle_gc: GCToggler
toggle_gc_postcollect: GCToggler

__all__ = ["get_all", "GCToggler", "toggle_gc", "toggle_gc_postcollect"]
