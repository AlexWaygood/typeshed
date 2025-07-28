"""
Greenlet-local objects.

This module is based on `_threading_local.py`__ from the standard
library of Python 3.4.

__ https://github.com/python/cpython/blob/3.4/Lib/_threading_local.py

Greenlet-local objects support the management of greenlet-local data.
If you have data that you want to be local to a greenlet, simply create
a greenlet-local object and use its attributes:

  >>> import gevent
  >>> from gevent.local import local
  >>> mydata = local()
  >>> mydata.number = 42
  >>> mydata.number
  42

You can also access the local-object's dictionary:

  >>> mydata.__dict__
  {'number': 42}
  >>> mydata.__dict__.setdefault('widgets', [])
  []
  >>> mydata.widgets
  []

What's important about greenlet-local objects is that their data are
local to a greenlet. If we access the data in a different greenlet:

  >>> log = []
  >>> def f():
  ...     items = list(mydata.__dict__.items())
  ...     items.sort()
  ...     log.append(items)
  ...     mydata.number = 11
  ...     log.append(mydata.number)
  >>> greenlet = gevent.spawn(f)
  >>> greenlet.join()
  >>> log
  [[], 11]

we get different data.  Furthermore, changes made in the other greenlet
don't affect data seen in this greenlet:

  >>> mydata.number
  42

Of course, values you get from a local object, including a __dict__
attribute, are for whatever greenlet was current at the time the
attribute was read.  For that reason, you generally don't want to save
these values across greenlets, as they apply only to the greenlet they
came from.

You can create custom local objects by subclassing the local class:

  >>> class MyLocal(local):
  ...     number = 2
  ...     initialized = False
  ...     def __init__(self, **kw):
  ...         if self.initialized:
  ...             raise SystemError('__init__ called too many times')
  ...         self.initialized = True
  ...         self.__dict__.update(kw)
  ...     def squared(self):
  ...         return self.number ** 2

This can be useful to support default values, methods and
initialization.  Note that if you define an __init__ method, it will be
called each time the local object is used in a separate greenlet.  This
is necessary to initialize each greenlet's dictionary.

Now if we create a local object:

  >>> mydata = MyLocal(color='red')

Now we have a default number:

  >>> mydata.number
  2

an initial color:

  >>> mydata.color
  'red'
  >>> del mydata.color

And a method that operates on the data:

  >>> mydata.squared()
  4

As before, we can access the data in a separate greenlet:

  >>> log = []
  >>> greenlet = gevent.spawn(f)
  >>> greenlet.join()
  >>> log
  [[('color', 'red'), ('initialized', True)], 11]

without affecting this greenlet's data:

  >>> mydata.number
  2
  >>> mydata.color
  Traceback (most recent call last):
  ...
  AttributeError: 'MyLocal' object has no attribute 'color'

Note that subclasses can define slots, but they are not greenlet
local. They are shared across greenlets::

  >>> class MyLocal(local):
  ...     __slots__ = 'number'

  >>> mydata = MyLocal()
  >>> mydata.number = 42
  >>> mydata.color = 'red'

So, the separate greenlet:

  >>> greenlet = gevent.spawn(f)
  >>> greenlet.join()

affects what we see:

  >>> mydata.number
  11

>>> del mydata

.. versionchanged:: 1.1a2
   Update the implementation to match Python 3.4 instead of Python 2.5.
   This results in locals being eligible for garbage collection as soon
   as their greenlet exits.

.. versionchanged:: 1.2.3
   Use a weak-reference to clear the greenlet link we establish in case
   the local object dies before the greenlet does.

.. versionchanged:: 1.3a1
   Implement the methods for attribute access directly, handling
   descriptors directly here. This allows removing the use of a lock
   and facilitates greatly improved performance.

.. versionchanged:: 1.3a1
   The ``__init__`` method of subclasses of ``local`` is no longer
   called with a lock held. CPython does not use such a lock in its
   native implementation. This could potentially show as a difference
   if code that uses multiple dependent attributes in ``__slots__``
   (which are shared across all greenlets) switches during ``__init__``.

"""

from typing import Any
from typing_extensions import Self

class local:
    """
    An object whose attributes are greenlet-local.
    """

    def __init__(self, *args: object, **kwargs: object) -> None: ...
    def __copy__(self) -> Self:
        """local.__copy__(self) -> local"""

    def __getattribute__(self, name: str) -> Any: ...
    def __delattr__(self, name: str) -> None: ...
    def __setattr__(self, name: str, value: Any) -> None: ...

__all__ = ["local"]
