import sys
import types
from _typeshed import Incomplete, ReadableBuffer, WriteableBuffer
from collections.abc import Callable, Hashable
from typing import Any, ClassVar, Literal, Protocol, SupportsIndex, TypeVar, final, overload
from typing_extensions import TypeAlias

_T = TypeVar("_T")

class _Allocator(Protocol):
    def __call__(self, cdecl: str | CType, init: Any = ...) -> _CDataBase: ...

__version__: str

FFI_CDECL: int
FFI_DEFAULT_ABI: int
RTLD_GLOBAL: int
RTLD_LAZY: int
RTLD_LOCAL: int
RTLD_NOW: int
if sys.platform == "linux":
    RTLD_DEEPBIND: int
if sys.platform != "win32":
    RTLD_NODELETE: int
    RTLD_NOLOAD: int

@final
class CField:
    bitshift: Incomplete
    bitsize: Incomplete
    flags: Incomplete
    offset: Incomplete
    type: Incomplete

@final
class CLibrary:
    def close_lib(self) -> None: ...
    def load_function(self, *args, **kwargs): ...
    def read_variable(self, *args, **kwargs): ...
    def write_variable(self, *args, **kwargs): ...

@final
class CType:
    abi: Incomplete
    args: Incomplete
    cname: Incomplete
    elements: Incomplete
    ellipsis: Incomplete
    fields: Incomplete
    item: Incomplete
    kind: Incomplete
    length: Incomplete
    relements: Incomplete
    result: Incomplete
    def __dir__(self): ...

@final
class Lib:
    def __dir__(self): ...

@final
class _CDataBase:
    """The internal base type for CData objects.  Use FFI.CData to access it.  Always check with isinstance(): subtypes are sometimes returned on CPython, for performance reasons."""

    __name__: ClassVar[str]
    def __add__(self, other):
        """Return self+value."""

    def __bool__(self) -> bool:
        """True if self else False"""

    def __call__(self, *args, **kwargs):
        """Call self as a function."""

    def __complex__(self) -> complex: ...
    def __delitem__(self, other) -> None:
        """Delete self[key]."""

    def __dir__(self): ...
    def __enter__(self): ...
    def __eq__(self, other): ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None): ...
    def __float__(self) -> float:
        """float(self)"""

    def __ge__(self, other): ...
    def __getitem__(self, index: SupportsIndex | slice):
        """Return self[key]."""

    def __gt__(self, other): ...
    def __hash__(self) -> int: ...
    def __int__(self) -> int:
        """int(self)"""

    def __iter__(self):
        """Implement iter(self)."""

    def __le__(self, other): ...
    def __len__(self) -> int:
        """Return len(self)."""

    def __lt__(self, other): ...
    def __ne__(self, other): ...
    def __radd__(self, other):
        """Return value+self."""

    def __rsub__(self, other):
        """Return value-self."""

    def __setitem__(self, index: SupportsIndex | slice, object) -> None:
        """Set self[key] to value."""

    def __sub__(self, other):
        """Return self-value."""

@final
class buffer:
    """ffi.buffer(cdata[, byte_size]):
    Return a read-write buffer object that references the raw C data
    pointed to by the given 'cdata'.  The 'cdata' must be a pointer or an
    array.  Can be passed to functions expecting a buffer, or directly
    manipulated with:

        buf[:]          get a copy of it in a regular string, or
        buf[idx]        as a single character
        buf[:] = ...
        buf[idx] = ...  change the content
    """

    __hash__: ClassVar[None]  # type: ignore[assignment]
    def __init__(self, *args, **kwargs) -> None: ...
    def __delitem__(self, other) -> None:
        """Delete self[key]."""

    def __eq__(self, other): ...
    def __ge__(self, other): ...
    def __getitem__(self, index):
        """Return self[key]."""

    def __gt__(self, other): ...
    def __le__(self, other): ...
    def __len__(self) -> int:
        """Return len(self)."""

    def __lt__(self, other): ...
    def __ne__(self, other): ...
    def __setitem__(self, index, object) -> None:
        """Set self[key] to value."""

# These aliases are to work around pyright complaints.
# Pyright doesn't like it when a class object is defined as an alias
# of a global object with the same name.
_tmp_CType = CType
_tmp_buffer = buffer

class FFI:
    CData: TypeAlias = _CDataBase
    CType: TypeAlias = _tmp_CType
    buffer: TypeAlias = _tmp_buffer  # noqa: Y042

    class error(Exception): ...
    NULL: ClassVar[CData]
    RTLD_GLOBAL: ClassVar[int]
    RTLD_LAZY: ClassVar[int]
    RTLD_LOCAL: ClassVar[int]
    RTLD_NOW: ClassVar[int]
    if sys.platform != "win32":
        RTLD_DEEPBIND: ClassVar[int]
        RTLD_NODELETE: ClassVar[int]
        RTLD_NOLOAD: ClassVar[int]

    errno: int

    def __init__(
        self,
        module_name: str = ...,
        _version: int = ...,
        _types: bytes = ...,
        _globals: tuple[bytes | int, ...] = ...,
        _struct_unions: tuple[tuple[bytes, ...], ...] = ...,
        _enums: tuple[bytes, ...] = ...,
        _typenames: tuple[bytes, ...] = ...,
        _includes: tuple[FFI, ...] = ...,
    ) -> None: ...
    @overload
    def addressof(self, cdata: CData, /, *field_or_index: str | int) -> CData:
        """Limited equivalent to the '&' operator in C:

        1. ffi.addressof(<cdata 'struct-or-union'>) returns a cdata that is a
        pointer to this struct or union.

        2. ffi.addressof(<cdata>, field-or-index...) returns the address of a
        field or array item inside the given structure or array, recursively
        in case of nested structures or arrays.

        3. ffi.addressof(<library>, "name") returns the address of the named
        function or global variable.
        """

    @overload
    def addressof(self, library: Lib, name: str, /) -> CData: ...
    def alignof(self, cdecl: str | CType | CData, /) -> int:
        """Return the natural alignment size in bytes of the argument.
        It can be a string naming a C type, or a 'cdata' instance.
        """

    @overload
    def callback(
        self,
        cdecl: str | CType,
        python_callable: None = ...,
        error: Any = ...,
        onerror: Callable[[Exception, Any, Any], None] | None = ...,
    ) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
        """Return a callback object or a decorator making such a callback object.
        'cdecl' must name a C function pointer type.  The callback invokes the
        specified 'python_callable' (which may be provided either directly or
        via a decorator).  Important: the callback object must be manually
        kept alive for as long as the callback may be invoked from the C code.
        """

    @overload
    def callback(
        self,
        cdecl: str | CType,
        python_callable: Callable[..., _T],
        error: Any = ...,
        onerror: Callable[[Exception, Any, Any], None] | None = ...,
    ) -> Callable[..., _T]: ...
    def cast(self, cdecl: str | CType, value: CData | int) -> CData:
        """Similar to a C cast: returns an instance of the named C
        type initialized with the given 'source'.  The source is
        casted between integers or pointers of any type.
        """

    def def_extern(
        self, name: str = ..., error: Any = ..., onerror: Callable[[Exception, Any, types.TracebackType], Any] = ...
    ) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
        """A decorator.  Attaches the decorated Python function to the C code
        generated for the 'extern "Python"' function of the same name.
        Calling the C function will then invoke the Python function.

        Optional arguments: 'name' is the name of the C function, if
        different from the Python function; and 'error' and 'onerror'
        handle what occurs if the Python function raises an exception
        (see the docs for details).
        """

    def dlclose(self, lib: Lib, /) -> None:
        """Close a library obtained with ffi.dlopen().  After this call, access to
        functions or variables from the library will fail (possibly with a
        segmentation fault).
        """
    if sys.platform == "win32":
        def dlopen(self, libpath: str | CData, flags: int = ..., /) -> Lib: ...
    else:
        def dlopen(self, libpath: str | CData | None = ..., flags: int = ..., /) -> Lib:
            """Load and return a dynamic library identified by 'name'.  The standard
            C library can be loaded by passing None.

            Note that functions and types declared with 'ffi.cdef()' are not
            linked to a particular library, just like C headers.  In the library
            we only look for the actual (untyped) symbols at the time of their
            first access.
            """

    @overload
    def from_buffer(self, cdecl: ReadableBuffer, require_writable: Literal[False] = ...) -> CData:
        """Return a <cdata 'char[]'> that points to the data of the given Python
        object, which must support the buffer interface.  Note that this is
        not meant to be used on the built-in types str or unicode
        (you can build 'char[]' arrays explicitly) but only on objects
        containing large quantities of raw data in some other format, like
        'array.array' or numpy arrays.
        """

    @overload
    def from_buffer(self, cdecl: WriteableBuffer, require_writable: Literal[True]) -> CData: ...
    @overload
    def from_buffer(self, cdecl: str | CType, python_buffer: ReadableBuffer, require_writable: Literal[False] = ...) -> CData: ...
    @overload
    def from_buffer(self, cdecl: str | CType, python_buffer: WriteableBuffer, require_writable: Literal[True]) -> CData: ...
    def from_handle(self, x: CData, /) -> Any:
        """Cast a 'void *' back to a Python object.  Must be used *only* on the
        pointers returned by new_handle(), and *only* as long as the exact
        cdata object returned by new_handle() is still alive (somewhere else
        in the program).  Failure to follow these rules will crash.
        """

    @overload
    def gc(self, cdata: CData, destructor: Callable[[CData], Any], size: int = ...) -> CData:
        """Return a new cdata object that points to the same data.
        Later, when this new cdata object is garbage-collected,
        'destructor(old_cdata_object)' will be called.

        The optional 'size' gives an estimate of the size, used to
        trigger the garbage collection more eagerly.  So far only used
        on PyPy.  It tells the GC that the returned object keeps alive
        roughly 'size' bytes of external memory.
        """

    @overload
    def gc(self, cdata: CData, destructor: None, size: int = ...) -> None: ...
    def getctype(self, cdecl: str | CType, replace_with: str = ...) -> str:
        """Return a string giving the C type 'cdecl', which may be itself a
        string or a <ctype> object.  If 'replace_with' is given, it gives
        extra text to append (or insert for more complicated C types), like a
        variable name, or '*' to get actually the C type 'pointer-to-cdecl'.
        """
    if sys.platform == "win32":
        def getwinerror(self, code: int = ...) -> tuple[int, str]: ...

    def init_once(self, func: Callable[[], Any], tag: Hashable) -> Any:
        """init_once(function, tag): run function() once.  More precisely,
        'function()' is called the first time we see a given 'tag'.

        The return value of function() is remembered and returned by the current
        and all future init_once() with the same tag.  If init_once() is called
        from multiple threads in parallel, all calls block until the execution
        of function() is done.  If function() raises an exception, it is
        propagated and nothing is cached.
        """

    def integer_const(self, name: str) -> int:
        """Get the value of an integer constant.

        'ffi.integer_const("xxx")' is equivalent to 'lib.xxx' if xxx names an
        integer constant.  The point of this function is limited to use cases
        where you have an 'ffi' object but not any associated 'lib' object.
        """

    def list_types(self) -> tuple[list[str], list[str], list[str]]:
        """Returns the user type names known to this FFI instance.
        This returns a tuple containing three lists of names:
        (typedef_names, names_of_structs, names_of_unions)
        """

    def memmove(self, dest: CData | WriteableBuffer, src: CData | ReadableBuffer, n: int) -> None:
        """ffi.memmove(dest, src, n) copies n bytes of memory from src to dest.

        Like the C function memmove(), the memory areas may overlap;
        apart from that it behaves like the C function memcpy().

        'src' can be any cdata ptr or array, or any Python buffer object.
        'dest' can be any cdata ptr or array, or a writable Python buffer
        object.  The size to copy, 'n', is always measured in bytes.

        Unlike other methods, this one supports all Python buffer including
        byte strings and bytearrays---but it still does not support
        non-contiguous buffers.
        """

    def new(self, cdecl: str | CType, init: Any = ...) -> CData:
        """Allocate an instance according to the specified C type and return a
        pointer to it.  The specified C type must be either a pointer or an
        array: ``new('X *')`` allocates an X and returns a pointer to it,
        whereas ``new('X[n]')`` allocates an array of n X'es and returns an
        array referencing it (which works mostly like a pointer, like in C).
        You can also use ``new('X[]', n)`` to allocate an array of a
        non-constant length n.

        The memory is initialized following the rules of declaring a global
        variable in C: by default it is zero-initialized, but an explicit
        initializer can be given which can be used to fill all or part of the
        memory.

        When the returned <cdata> object goes out of scope, the memory is
        freed.  In other words the returned <cdata> object has ownership of
        the value of type 'cdecl' that it points to.  This means that the raw
        data can be used as long as this object is kept alive, but must not be
        used for a longer time.  Be careful about that when copying the
        pointer to the memory somewhere else, e.g. into another structure.
        """

    @overload
    def new_allocator(self, alloc: None = ..., free: None = ..., should_clear_after_alloc: bool = ...) -> _Allocator:
        """Return a new allocator, i.e. a function that behaves like ffi.new()
        but uses the provided low-level 'alloc' and 'free' functions.

        'alloc' is called with the size as argument.  If it returns NULL, a
        MemoryError is raised.  'free' is called with the result of 'alloc'
        as argument.  Both can be either Python functions or directly C
        functions.  If 'free' is None, then no free function is called.
        If both 'alloc' and 'free' are None, the default is used.

        If 'should_clear_after_alloc' is set to False, then the memory
        returned by 'alloc' is assumed to be already cleared (or you are
        fine with garbage); otherwise CFFI will clear it.
        """

    @overload
    def new_allocator(
        self, alloc: Callable[[int], CData], free: None = ..., should_clear_after_alloc: bool = ...
    ) -> _Allocator: ...
    @overload
    def new_allocator(
        self, alloc: Callable[[int], CData], free: Callable[[CData], Any], should_clear_after_alloc: bool = ...
    ) -> _Allocator: ...
    def new_handle(self, x: Any, /) -> CData:
        """Return a non-NULL cdata of type 'void *' that contains an opaque
        reference to the argument, which can be any Python object.  To cast it
        back to the original object, use from_handle().  You must keep alive
        the cdata object returned by new_handle()!
        """

    def offsetof(self, cdecl: str | CType, field_or_index: str | int, /, *__fields_or_indexes: str | int) -> int:
        """Return the offset of the named field inside the given structure or
        array, which must be given as a C type name.  You can give several
        field names in case of nested structures.  You can also give numeric
        values which correspond to array items, in case of an array type.
        """

    def release(self, cdata: CData, /) -> None:
        """Release now the resources held by a 'cdata' object from ffi.new(),
        ffi.gc() or ffi.from_buffer().  The cdata object must not be used
        afterwards.

        'ffi.release(cdata)' is equivalent to 'cdata.__exit__()'.

        Note that on CPython this method has no effect (so far) on objects
        returned by ffi.new(), because the memory is allocated inline with the
        cdata object and cannot be freed independently.  It might be fixed in
        future releases of cffi.
        """

    def sizeof(self, cdecl: str | CType | CData, /) -> int:
        """Return the size in bytes of the argument.
        It can be a string naming a C type, or a 'cdata' instance.
        """

    def string(self, cdata: CData, maxlen: int = -1) -> bytes | str:
        """Return a Python string (or unicode string) from the 'cdata'.  If
        'cdata' is a pointer or array of characters or bytes, returns the
        null-terminated string.  The returned string extends until the first
        null character, or at most 'maxlen' characters.  If 'cdata' is an
        array then 'maxlen' defaults to its length.

        If 'cdata' is a pointer or array of wchar_t, returns a unicode string
        following the same rules.

        If 'cdata' is a single character or byte or a wchar_t, returns it as a
        string or unicode string.

        If 'cdata' is an enum, returns the value of the enumerator as a
        string, or 'NUMBER' if the value is out of range.
        """

    def typeof(self, cdecl: str | CData, /) -> CType:
        """Parse the C type given as a string and return the
        corresponding <ctype> object.
        It can also be used on 'cdata' instance to get its C type.
        """

    def unpack(self, cdata: CData, length: int) -> bytes | str | list[Any]:
        """Unpack an array of C data of the given length,
        returning a Python string/unicode/list.

        If 'cdata' is a pointer to 'char', returns a byte string.
        It does not stop at the first null.  This is equivalent to:
        ffi.buffer(cdata, length)[:]

        If 'cdata' is a pointer to 'wchar_t', returns a unicode string.
        'length' is measured in wchar_t's; it is not the size in bytes.

        If 'cdata' is a pointer to anything else, returns a list of
        'length' items.  This is a faster equivalent to:
        [cdata[i] for i in range(length)]
        """

def alignof(cdecl: CType, /) -> int: ...
def callback(
    cdecl: CType,
    python_callable: Callable[..., _T],
    error: Any = ...,
    onerror: Callable[[Exception, Any, Any], None] | None = ...,
    /,
) -> Callable[..., _T]: ...
def cast(cdecl: CType, value: _CDataBase, /) -> _CDataBase: ...
def complete_struct_or_union(
    cdecl: CType,
    fields: list[tuple[str, CType, int, int]],
    ignored: Any,
    total_size: int,
    total_alignment: int,
    sflags: int,
    pack: int,
    /,
) -> None: ...
@overload
def from_buffer(cdecl: CType, python_buffer: ReadableBuffer, /, require_writable: Literal[False] = ...) -> _CDataBase: ...
@overload
def from_buffer(cdecl: CType, python_buffer: WriteableBuffer, /, require_writable: Literal[True]) -> _CDataBase: ...
def from_handle(x: _CDataBase, /) -> Any: ...
@overload
def gcp(cdata: _CDataBase, destructor: Callable[[_CDataBase], Any], size: int = ...) -> _CDataBase: ...
@overload
def gcp(cdata: _CDataBase, destructor: None, size: int = ...) -> None: ...
def get_errno() -> int: ...
def getcname(cdecl: CType, replace_with: str, /) -> str: ...

if sys.platform == "win32":
    def getwinerror(code: int = ...) -> tuple[int, str]: ...

if sys.platform == "win32":
    def load_library(libpath: str | _CDataBase, flags: int = ..., /) -> CLibrary: ...

else:
    def load_library(libpath: str | _CDataBase | None = ..., flags: int = ..., /) -> CLibrary: ...

def memmove(dest: _CDataBase | WriteableBuffer, src: _CDataBase | ReadableBuffer, n: int) -> None: ...
def new_array_type(cdecl: CType, length: int | None, /) -> CType: ...
def new_enum_type(name: str, enumerators: tuple[str, ...], enumvalues: tuple[Any, ...], basetype: CType, /) -> CType: ...
def new_function_type(args: tuple[CType, ...], result: CType, ellipsis: int, abi: int, /) -> CType: ...
def new_pointer_type(cdecl: CType, /) -> CType: ...
def new_primitive_type(name: str, /) -> CType: ...
def new_struct_type(name: str, /) -> CType: ...
def new_union_type(name: str, /) -> CType: ...
def new_void_type() -> CType: ...
def newp(cdecl: CType, init: Any = ..., /) -> _CDataBase: ...
def newp_handle(cdecl: CType, x: Any, /) -> _CDataBase: ...
def rawaddressof(cdecl: CType, cdata: _CDataBase, offset: int, /) -> _CDataBase: ...
def release(cdata: _CDataBase, /) -> None: ...
def set_errno(errno: int, /) -> None: ...
def sizeof(cdecl: CType | _CDataBase, /) -> int: ...
def string(cdata: _CDataBase, maxlen: int) -> bytes | str: ...
def typeof(cdata: _CDataBase, /) -> CType: ...
def typeoffsetof(cdecl: CType, fieldname: str | int, following: bool = ..., /) -> tuple[CType, int]: ...
def unpack(cdata: _CDataBase, length: int) -> bytes | str | list[Any]: ...
