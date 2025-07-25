import sys
import types
from _typeshed import ReadableBuffer, WriteableBuffer
from collections.abc import Callable, Hashable
from typing import Any, Literal, TypeVar, overload
from typing_extensions import TypeAlias

import _cffi_backend
from setuptools._distutils.extension import Extension

_T = TypeVar("_T")

basestring: TypeAlias = str  # noqa: Y042

class FFI:
    '''
    The main top-level class that you instantiate once, or once per module.

    Example usage:

        ffi = FFI()
        ffi.cdef("""
            int printf(const char *, ...);
        """)

        C = ffi.dlopen(None)   # standard library
        -or-
        C = ffi.verify()  # use a C compiler: verify the decl above is right

        C.printf("hello, %s!\\n", ffi.new("char[]", "world"))
    '''

    CData: TypeAlias = _cffi_backend._CDataBase
    CType: TypeAlias = _cffi_backend.CType
    buffer: TypeAlias = _cffi_backend.buffer  # noqa: Y042

    BVoidP: CType
    BCharA: CType
    NULL: CType
    errno: int

    def __init__(self, backend: types.ModuleType | None = None) -> None:
        """Create an FFI instance.  The 'backend' argument is used to
        select a non-default backend, mostly for tests.
        """

    def cdef(self, csource: str, override: bool = False, packed: bool = False, pack: int | None = None) -> None:
        """Parse the given C source.  This registers all declared functions,
        types, and global variables.  The functions and global variables can
        then be accessed via either 'ffi.dlopen()' or 'ffi.verify()'.
        The types can be used in 'ffi.new()' and other functions.
        If 'packed' is specified as True, all structs declared inside this
        cdef are packed, i.e. laid out without any field alignment at all.
        Alternatively, 'pack' can be a small integer, and requests for
        alignment greater than that are ignored (pack=1 is equivalent to
        packed=True).
        """

    def embedding_api(self, csource: str, packed: bool = False, pack: bool | int | None = None) -> None: ...

    if sys.platform == "win32":
        def dlopen(self, name: str, flags: int = ...) -> _cffi_backend.Lib: ...
    else:
        def dlopen(self, name: str | None, flags: int = ...) -> _cffi_backend.Lib:
            """Load and return a dynamic library identified by 'name'.
            The standard C library can be loaded by passing None.
            Note that functions and types declared by 'ffi.cdef()' are not
            linked to a particular library, just like C headers; in the
            library we only look for the actual (untyped) symbols.
            """

    def dlclose(self, lib: _cffi_backend.Lib) -> None:
        """Close a library obtained with ffi.dlopen().  After this call,
        access to functions or variables from the library will fail
        (possibly with a segmentation fault).
        """

    def typeof(self, cdecl: str | CData | types.BuiltinFunctionType | types.FunctionType) -> CType:
        """Parse the C type given as a string and return the
        corresponding <ctype> object.
        It can also be used on 'cdata' instance to get its C type.
        """

    def sizeof(self, cdecl: str | CData) -> int:
        """Return the size in bytes of the argument.  It can be a
        string naming a C type, or a 'cdata' instance.
        """

    def alignof(self, cdecl: str | CData) -> int:
        """Return the natural alignment size in bytes of the C type
        given as a string.
        """

    def offsetof(self, cdecl: str | CData, *fields_or_indexes: str | int) -> int:
        """Return the offset of the named field inside the given
        structure or array, which must be given as a C type name.
        You can give several field names in case of nested structures.
        You can also give numeric values which correspond to array
        items, in case of an array type.
        """

    def new(self, cdecl: str | CType, init=None) -> CData:
        """Allocate an instance according to the specified C type and
        return a pointer to it.  The specified C type must be either a
        pointer or an array: ``new('X *')`` allocates an X and returns
        a pointer to it, whereas ``new('X[n]')`` allocates an array of
        n X'es and returns an array referencing it (which works
        mostly like a pointer, like in C).  You can also use
        ``new('X[]', n)`` to allocate an array of a non-constant
        length n.

        The memory is initialized following the rules of declaring a
        global variable in C: by default it is zero-initialized, but
        an explicit initializer can be given which can be used to
        fill all or part of the memory.

        When the returned <cdata> object goes out of scope, the memory
        is freed.  In other words the returned <cdata> object has
        ownership of the value of type 'cdecl' that it points to.  This
        means that the raw data can be used as long as this object is
        kept alive, but must not be used for a longer time.  Be careful
        about that when copying the pointer to the memory somewhere
        else, e.g. into another structure.
        """

    def new_allocator(
        self,
        alloc: Callable[[int], CData] | None = None,
        free: Callable[[CData], Any] | None = None,
        should_clear_after_alloc: bool = True,
    ) -> _cffi_backend._Allocator:
        """Return a new allocator, i.e. a function that behaves like ffi.new()
        but uses the provided low-level 'alloc' and 'free' functions.

        'alloc' is called with the size as argument.  If it returns NULL, a
        MemoryError is raised.  'free' is called with the result of 'alloc'
        as argument.  Both can be either Python function or directly C
        functions.  If 'free' is None, then no free function is called.
        If both 'alloc' and 'free' are None, the default is used.

        If 'should_clear_after_alloc' is set to False, then the memory
        returned by 'alloc' is assumed to be already cleared (or you are
        fine with garbage); otherwise CFFI will clear it.
        """

    def cast(self, cdecl: str | CType, source: CData | int) -> CData:
        """Similar to a C cast: returns an instance of the named C
        type initialized with the given 'source'.  The source is
        casted between integers or pointers of any type.
        """

    def string(self, cdata: CData, maxlen: int = -1) -> bytes | str:
        """Return a Python string (or unicode string) from the 'cdata'.
        If 'cdata' is a pointer or array of characters or bytes, returns
        the null-terminated string.  The returned string extends until
        the first null character, or at most 'maxlen' characters.  If
        'cdata' is an array then 'maxlen' defaults to its length.

        If 'cdata' is a pointer or array of wchar_t, returns a unicode
        string following the same rules.

        If 'cdata' is a single character or byte or a wchar_t, returns
        it as a string or unicode string.

        If 'cdata' is an enum, returns the value of the enumerator as a
        string, or 'NUMBER' if the value is out of range.
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

    @overload
    def from_buffer(self, cdecl: ReadableBuffer, require_writable: Literal[False] = False) -> CData:
        """Return a cdata of the given type pointing to the data of the
        given Python object, which must support the buffer interface.
        Note that this is not meant to be used on the built-in types
        str or unicode (you can build 'char[]' arrays explicitly)
        but only on objects containing large quantities of raw data
        in some other format, like 'array.array' or numpy arrays.

        The first argument is optional and default to 'char[]'.
        """

    @overload
    def from_buffer(self, cdecl: WriteableBuffer, require_writable: Literal[True]) -> CData: ...
    @overload
    def from_buffer(
        self, cdecl: str | CType, python_buffer: ReadableBuffer, require_writable: Literal[False] = False
    ) -> CData: ...
    @overload
    def from_buffer(self, cdecl: str | CType, python_buffer: WriteableBuffer, require_writable: Literal[True]) -> CData: ...
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

    @overload
    def callback(
        self,
        cdecl: str | CType,
        python_callable: None = None,
        error: Any = None,
        onerror: Callable[[Exception, Any, Any], None] | None = None,
    ) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
        """Return a callback object or a decorator making such a
        callback object.  'cdecl' must name a C function pointer type.
        The callback invokes the specified 'python_callable' (which may
        be provided either directly or via a decorator).  Important: the
        callback object must be manually kept alive for as long as the
        callback may be invoked from the C level.
        """

    @overload
    def callback(
        self,
        cdecl: str | CType,
        python_callable: Callable[..., _T],
        error: Any = None,
        onerror: Callable[[Exception, Any, Any], None] | None = None,
    ) -> Callable[..., _T]: ...
    def getctype(self, cdecl: str | CType, replace_with: str = "") -> str:
        """Return a string giving the C type 'cdecl', which may be itself
        a string or a <ctype> object.  If 'replace_with' is given, it gives
        extra text to append (or insert for more complicated C types), like
        a variable name, or '*' to get actually the C type 'pointer-to-cdecl'.
        """

    @overload
    def gc(self, cdata: CData, destructor: Callable[[CData], Any], size: int = 0) -> CData:
        """Return a new cdata object that points to the same
        data.  Later, when this new cdata object is garbage-collected,
        'destructor(old_cdata_object)' will be called.

        The optional 'size' gives an estimate of the size, used to
        trigger the garbage collection more eagerly.  So far only used
        on PyPy.  It tells the GC that the returned object keeps alive
        roughly 'size' bytes of external memory.
        """

    @overload
    def gc(self, cdata: CData, destructor: None, size: int = 0) -> None: ...
    def verify(self, source: str = "", tmpdir: str | None = None, **kwargs: Any) -> _cffi_backend.Lib:
        """Verify that the current ffi signatures compile on this
        machine, and return a dynamic library object.  The dynamic
        library can be used to call functions and access global
        variables declared in this 'ffi'.  The library is compiled
        by the C compiler: it gives you C-level API compatibility
        (including calling macros).  This is unlike 'ffi.dlopen()',
        which requires binary compatibility in the signatures.
        """
    # Technically exists on all OSs, but crashes on all but Windows. So we hide it in stubs
    if sys.platform == "win32":
        def getwinerror(self, code: int = -1) -> tuple[int, str] | None: ...

    def addressof(self, cdata: CData, *fields_or_indexes: str | int) -> CData:
        """Return the address of a <cdata 'struct-or-union'>.
        If 'fields_or_indexes' are given, returns the address of that
        field or array item in the structure or array, recursively in
        case of nested structures.
        """

    def include(self, ffi_to_include: FFI) -> None:
        """Includes the typedefs, structs, unions and enums defined
        in another FFI instance.  Usage is similar to a #include in C,
        where a part of the program might include types defined in
        another part for its own usage.  Note that the include()
        method has no effect on functions, constants and global
        variables, which must anyway be accessed directly from the
        lib object returned by the original FFI instance.
        """

    def new_handle(self, x: Any) -> CData: ...
    def from_handle(self, x: CData) -> Any: ...
    def release(self, x: CData) -> None: ...
    def set_unicode(self, enabled_flag: bool) -> None:
        """Windows: if 'enabled_flag' is True, enable the UNICODE and
        _UNICODE defines in C, and declare the types like TCHAR and LPTCSTR
        to be (pointers to) wchar_t.  If 'enabled_flag' is False,
        declare these types to be (pointers to) plain 8-bit characters.
        This is mostly for backward compatibility; you usually want True.
        """

    def set_source(self, module_name: str, source: str | None, source_extension: str = ".c", **kwds: Any) -> None: ...
    def set_source_pkgconfig(
        self, module_name: str, pkgconfig_libs: list[str], source: str, source_extension: str = ".c", **kwds: Any
    ) -> None: ...
    def distutils_extension(self, tmpdir: str = "build", verbose: bool = True) -> Extension: ...
    def emit_c_code(self, filename: str) -> None: ...
    def emit_python_code(self, filename: str) -> None: ...
    def compile(self, tmpdir: str = ".", verbose: int = 0, target: str | None = None, debug: bool | None = None) -> str:
        """The 'target' argument gives the final file name of the
        compiled DLL.  Use '*' to force distutils' choice, suitable for
        regular CPython C API modules.  Use a file name ending in '.*'
        to ask for the system's default extension for dynamic libraries
        (.so/.dll/.dylib).

        The default is '*' when building a non-embedded C API extension,
        and (module_name + '.*') when building an embedded library.
        """

    def init_once(self, func: Callable[[], Any], tag: Hashable) -> Any: ...
    def embedding_init_code(self, pysource: str) -> None: ...
    def def_extern(self, *args: Any, **kwds: Any) -> None: ...
    def list_types(self) -> tuple[list[str], list[str], list[str]]:
        """Returns the user type names known to this FFI instance.
        This returns a tuple containing three lists of names:
        (typedef_names, names_of_structs, names_of_unions)
        """
