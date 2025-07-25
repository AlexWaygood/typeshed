"""
A fast Python wrapper around Lua and LuaJIT2.
"""

from _typeshed import MaybeNone
from collections.abc import Callable, Iterator
from typing import Any, Final, Generic, TypeVar, type_check_only

__all__ = [
    "LUA_VERSION",
    "LUA_MAXINTEGER",
    "LUA_MININTEGER",
    "LuaRuntime",
    "LuaError",
    "LuaSyntaxError",
    "LuaMemoryError",
    "as_itemgetter",
    "as_attrgetter",
    "lua_type",
    "unpacks_lua_table",
    "unpacks_lua_table_method",
]

LUA_MAXINTEGER: Final[int]
LUA_MININTEGER: Final[int]
LUA_VERSION: Final[tuple[int, int]]

# cyfunction object
as_attrgetter: Callable[[object], object]
as_itemgetter: Callable[[object], object]

# cyfunction object
lua_type: Callable[[object], str | MaybeNone]

# cyfunction object as decorator
unpacks_lua_table: Callable[[Callable[..., Any]], Callable[..., Any]]
unpacks_lua_table_method: Callable[[Callable[..., Any]], Callable[..., Any]]

# inner classes

@type_check_only
class _LuaIter:
    def __iter__(self) -> Iterator[object]: ...

@type_check_only
class _LuaTable:
    def keys(self) -> _LuaIter: ...
    def values(self) -> _LuaIter: ...
    def items(self) -> _LuaIter: ...

@type_check_only
class _LuaNoGC: ...

@type_check_only
class _LuaObject: ...

# classes

_bint = TypeVar("_bint", bool, int)

class FastRLock(Generic[_bint]):
    """Fast, re-entrant locking.

    Under uncongested conditions, the lock is never acquired but only
    counted.  Only when a second thread comes in and notices that the
    lock is needed, it acquires the lock and notifies the first thread
    to release it when it's done.  This is all made possible by the
    wonderful GIL.
    """

    # @classmethod
    # def __init__(cls, /, *args: Any, **kwargs: Any) -> None: ...
    def acquire(self, blocking: _bint = True) -> _bint:
        """FastRLock.acquire(self, bool blocking=True)"""

    def release(self) -> None:
        """FastRLock.release(self)"""

    def __enter__(self) -> _bint:
        """FastRLock.__enter__(self)"""

    def __exit__(self, t: object, v: object, tb: object) -> None:
        """FastRLock.__exit__(self, t, v, tb)"""

class LuaError(Exception):
    """Base class for errors in the Lua runtime."""

class LuaSyntaxError(LuaError):
    """Syntax error in Lua code."""

class LuaMemoryError(LuaError, MemoryError):
    """Memory error in Lua code."""

class LuaRuntime:
    """The main entry point to the Lua runtime.

    Available options:

    * ``encoding``: the string encoding, defaulting to UTF-8.  If set
      to ``None``, all string values will be returned as byte strings.
      Otherwise, they will be decoded to unicode strings on the way
      from Lua to Python and unicode strings will be encoded on the
      way to Lua.  Note that ``str()`` calls on Lua objects will
      always return a unicode object.

    * ``source_encoding``: the encoding used for Lua code, defaulting to
      the string encoding or UTF-8 if the string encoding is ``None``.

    * ``attribute_filter``: filter function for attribute access
      (get/set).  Must have the signature ``func(obj, attr_name,
      is_setting)``, where ``is_setting`` is True when the attribute
      is being set.  If provided, the function will be called for all
      Python object attributes that are being accessed from Lua code.
      Normally, it should return an attribute name that will then be
      used for the lookup.  If it wants to prevent access, it should
      raise an ``AttributeError``.  Note that Lua does not guarantee
      that the names will be strings.  (New in Lupa 0.20)

    * ``attribute_handlers``: like ``attribute_filter`` above, but
      handles the getting/setting itself rather than giving hints
      to the LuaRuntime.  This must be a 2-tuple, ``(getter, setter)``
      where ``getter`` has the signature ``func(obj, attr_name)``
      and either returns the value for ``obj.attr_name`` or raises an
      ``AttributeError``  The function ``setter`` has the signature
      ``func(obj, attr_name, value)`` and may raise an ``AttributeError``.
      The return value of the setter is unused.  (New in Lupa 1.0)

    * ``register_eval``: should Python's ``eval()`` function be available
      to Lua code as ``python.eval()``?  Note that this does not remove it
      from the builtins.  Use an ``attribute_filter`` function for that.
      (default: True)

    * ``register_builtins``: should Python's builtins be available to Lua
      code as ``python.builtins.*``?  Note that this does not prevent access
      to the globals available as special Python function attributes, for
      example.  Use an ``attribute_filter`` function for that.
      (default: True, new in Lupa 1.2)

    * ``unpack_returned_tuples``: should Python tuples be unpacked in Lua?
      If ``py_fun()`` returns ``(1, 2, 3)``, then does ``a, b, c = py_fun()``
      give ``a == 1 and b == 2 and c == 3`` or does it give
      ``a == (1,2,3), b == nil, c == nil``?  ``unpack_returned_tuples=True``
      gives the former.
      (default: False, new in Lupa 0.21)

    * ``overflow_handler``: function for handling Python integers overflowing
      Lua integers. Must have the signature ``func(obj)``. If provided, the
      function will be called when a Python integer (possibly of arbitrary
      precision type) is too large to fit in a fixed-precision Lua integer.
      Normally, it should return the now well-behaved object that can be
      converted/wrapped to a Lua type. If the object cannot be precisely
      represented in Lua, it should raise an ``OverflowError``.

    * ``max_memory``: max memory usage this LuaRuntime can use in bytes.
      If max_memory is None, the default lua allocator is used and calls to
      ``set_max_memory(limit)`` will fail with a ``LuaMemoryError``.
      Note: Not supported on 64bit LuaJIT.
      (default: None, i.e. no limitation. New in Lupa 2.0)

    Example usage::

      >>> from lupa import LuaRuntime
      >>> lua = LuaRuntime()

      >>> lua.eval('1+1')
      2

      >>> lua_func = lua.eval('function(f, n) return f(n) end')

      >>> def py_add1(n): return n+1
      >>> lua_func(py_add1, 2)
      3
    """

    lua_implementation: Final[str]
    lua_version: Final[tuple[int, int]]

    # @classmethod
    # def __cinit__(cls, unpack_return_tuples: bool) -> None: ...
    # def add_pending_unref(self, ref: int) -> None: ...
    # def clean_up_pending_unrefs(self) -> int: ...
    def get_max_memory(self, total: bool = False) -> int | MaybeNone:
        """LuaRuntime.get_max_memory(self, total=False)

        Maximum memory allowed to be used by this LuaRuntime.
        0 indicates no limit meanwhile None indicates that the default lua
        allocator is being used and ``set_max_memory()`` cannot be used.

        If ``total`` is True, the base memory used by the lua runtime
        will be included in the limit.
        """

    def get_memory_used(self, total: bool = False) -> int | MaybeNone:
        """LuaRuntime.get_memory_used(self, total=False)

        Memory currently in use.
        This is None if the default lua allocator is used and 0 if
        ``max_memory`` is 0.

        If ``total`` is True, the base memory used by the lua runtime
        will be included.
        """
    # def reraise_on_exceptions(self) -> int: ...
    # def store_raised_exception(self, L: object, lua_error_msg: str) -> None: ...  # unannotated
    def eval(self, lua_code: str, *args: Any, name: str | None = None, mode: str | None = None) -> object:
        """LuaRuntime.eval(self, lua_code, *args, name=None, mode=None)

        Evaluate a Lua expression passed in a string.

        The 'name' argument can be used to override the name printed in error messages.

        The 'mode' argument specifies the input type.  By default, both source code and
        pre-compiled byte code is allowed (mode='bt').  It can be restricted to source
        code with mode='t' and to byte code with mode='b'.  This has no effect on Lua 5.1.
        """

    def execute(self, lua_code: str, *args: Any, name: str | None = None, mode: str | None = None) -> object:
        """LuaRuntime.execute(self, lua_code, *args, name=None, mode=None)

        Execute a Lua program passed in a string.

        The 'name' argument can be used to override the name printed in error messages.

        The 'mode' argument specifies the input type.  By default, both source code and
        pre-compiled byte code is allowed (mode='bt').  It can be restricted to source
        code with mode='t' and to byte code with mode='b'.  This has no effect on Lua 5.1.
        """

    def compile(self, lua_code: str, name: str | None = None, mode: str | None = None) -> Callable[..., object]:
        """LuaRuntime.compile(self, lua_code, name=None, mode=None)

        Compile a Lua program into a callable Lua function.

        The 'name' argument can be used to override the name printed in error messages.

        The 'mode' argument specifies the input type.  By default, both source code and
        pre-compiled byte code is allowed (mode='bt').  It can be restricted to source
        code with mode='t' and to byte code with mode='b'.  This has no effect on Lua 5.1.
        """

    def require(self, modulename: str) -> object:
        """LuaRuntime.require(self, modulename)

        Load a Lua library into the runtime.
        """

    def globals(self) -> _LuaTable:
        """LuaRuntime.globals(self)

        Return the globals defined in this Lua runtime as a Lua
        table.
        """

    def table(self, *items: Any, **kwargs: Any) -> _LuaTable:
        """LuaRuntime.table(self, *items, **kwargs)

        Create a new table with the provided items.  Positional
        arguments are placed in the table in order, keyword arguments
        are set as key-value pairs.
        """

    def table_from(self, *args: Any, recursive: bool = ...) -> _LuaTable:
        """LuaRuntime.table_from(self, *args, bool recursive=False)

        Create a new table from Python mapping or iterable.

        table_from() accepts either a dict/mapping or an iterable with items.
        Items from dicts are set as key-value pairs; items from iterables
        are placed in the table in order.

        Nested mappings / iterables are passed to Lua as userdata
        (wrapped Python objects) by default.  If `recursive` is True,
        they are converted to Lua tables recursively, handling loops
        and duplicates via identity de-duplication.
        """

    def nogc(self) -> _LuaNoGC:
        """LuaRuntime.nogc(self)

        Return a context manager that temporarily disables the Lua garbage collector.
        """

    def gccollect(self) -> None:
        """LuaRuntime.gccollect(self)

        Run a full pass of the Lua garbage collector.
        """

    def set_max_memory(self, max_memory: int, total: bool = False) -> None:
        """LuaRuntime.set_max_memory(self, size_t max_memory, total=False)

        Set maximum allowed memory for this LuaRuntime.

        If `max_memory` is 0, there will be no limit.
        If ``total`` is True, the base memory used by the LuaRuntime itself
        will be included in the memory limit.

        If max_memory was set to None during creation, this will raise a
        RuntimeError.
        """

    def set_overflow_handler(self, overflow_handler: Callable[..., None]) -> None:
        """LuaRuntime.set_overflow_handler(self, overflow_handler)

        Set the overflow handler function that is called on failures to pass large numbers to Lua.
        """
    # def register_py_object(self, cname: str, pyname: str, obj: object) -> int: ...
    # def init_python_lib(self, register_eval: bool, register_builtins: bool) -> int: ...
