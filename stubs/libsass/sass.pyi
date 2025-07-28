""":mod:`sass` --- Binding of ``libsass``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This simple C extension module provides a very simple binding of ``libsass``,
which is written in C/C++.  It contains only one function and one exception
type.

>>> import sass
>>> sass.compile(string='a { b { color: blue; } }')
'a b {
  color: blue; }
'

"""

import enum
from _typeshed import ConvertibleToFloat, SupportsKeysAndGetItem
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence, Set as AbstractSet
from typing import Any, Generic, Literal, NamedTuple, TypeVar, overload, type_check_only
from typing_extensions import ParamSpec, Self, TypeAlias

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)
_P = ParamSpec("_P")
_Mode: TypeAlias = Literal["string", "filename", "dirname"]
_OutputStyle: TypeAlias = Literal["nested", "expanded", "compact", "compressed"]
_CustomFunctions: TypeAlias = Mapping[str, Callable[..., Any]] | Sequence[Callable[..., Any]] | AbstractSet[Callable[..., Any]]
_ImportCallbackRet: TypeAlias = (
    list[tuple[str, str, str]] | list[tuple[str, str]] | list[tuple[str]] | list[tuple[str, ...]] | None
)
_ImportCallback: TypeAlias = Callable[[str], _ImportCallbackRet] | Callable[[str, str], _ImportCallbackRet]

__version__: str
libsass_version: str
OUTPUT_STYLES: dict[str, int]
SOURCE_COMMENTS: dict[str, int]
MODES: frozenset[_Mode]

class CompileError(ValueError):
    """The exception type that is raised by :func:`compile()`.
    It is a subtype of :exc:`exceptions.ValueError`.
    """

    def __init__(self, msg: str) -> None: ...

# _P needs to be positional only and can't contain varargs, but there is no way to express that
# the arguments also need
class SassFunction(Generic[_P, _T]):
    """Custom function for Sass.  It can be instantiated using
    :meth:`from_lambda()` and :meth:`from_named_function()` as well.

    :param name: the function name
    :type name: :class:`str`
    :param arguments: the argument names
    :type arguments: :class:`collections.abc.Sequence`
    :param callable_: the actual function to be called
    :type callable_: :class:`collections.abc.Callable`

    .. versionadded:: 0.7.0

    """

    @classmethod
    def from_lambda(cls, name: str, lambda_: Callable[_P, _T]) -> SassFunction[_P, _T]:
        """Make a :class:`SassFunction` object from the given ``lambda_``
        function.  Since lambda functions don't have their name, it need
        its ``name`` as well.  Arguments are automatically inspected.

        :param name: the function name
        :type name: :class:`str`
        :param lambda_: the actual lambda function to be called
        :type lambda_: :class:`types.LambdaType`
        :returns: a custom function wrapper of the ``lambda_`` function
        :rtype: :class:`SassFunction`

        """

    @classmethod
    def from_named_function(cls, function: Callable[_P, _T]) -> SassFunction[_P, _T]:
        """Make a :class:`SassFunction` object from the named ``function``.
        Function name and arguments are automatically inspected.

        :param function: the named function to be called
        :type function: :class:`types.FunctionType`
        :returns: a custom function wrapper of the ``function``
        :rtype: :class:`SassFunction`

        """
    name: str
    arguments: tuple[str, ...]
    callable_: Callable[_P, _T]
    def __init__(self, name: str, arguments: Sequence[str], callable_: Callable[_P, _T]) -> None: ...
    @property
    def signature(self) -> str:
        """Signature string of the function."""

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...

@overload
def compile(
    *,
    string: str,
    output_style: _OutputStyle = "nested",
    source_comments: bool = False,
    source_map_contents: bool = False,
    source_map_embed: bool = False,
    omit_source_map_url: bool = False,
    source_map_root: str | None = None,
    include_paths: Sequence[str] = (),
    precision: int = 5,
    custom_functions: _CustomFunctions = (),
    indented: bool = False,
    importers: Iterable[tuple[int, _ImportCallback]] | None = None,
) -> str:
    """There are three modes of parameters :func:`compile()` can take:
``string``, ``filename``, and ``dirname``.

The ``string`` parameter is the most basic way to compile Sass.
It simply takes a string of Sass code, and then returns a compiled
CSS string.

:param string: Sass source code to compile.  it's exclusive to
               ``filename`` and ``dirname`` parameters
:type string: :class:`str`
:param output_style: an optional coding style of the compiled result.
                     choose one of: ``'nested'`` (default), ``'expanded'``,
                     ``'compact'``, ``'compressed'``
:type output_style: :class:`str`
:param source_comments: whether to add comments about source lines.
                        :const:`False` by default
:type source_comments: :class:`bool`
:param source_map_contents: embed include contents in map
:type source_map_contents: :class:`bool`
:param source_map_embed: embed sourceMappingUrl as data URI
:type source_map_embed: :class:`bool`
:param omit_source_map_url: omit source map URL comment from output
:type omit_source_map_url: :class:`bool`
:param source_map_root: base path, will be emitted in source map as is
:type source_map_root: :class:`str`
:param include_paths: an optional list of paths to find ``@import``\\ ed
                      Sass/CSS source files
:type include_paths: :class:`collections.abc.Sequence`
:param precision: optional precision for numbers. :const:`5` by default.
:type precision: :class:`int`
:param custom_functions: optional mapping of custom functions.
                         see also below `custom functions
                         <custom-functions_>`_ description
:type custom_functions: :class:`set`,
                        :class:`collections.abc.Sequence`,
                        :class:`collections.abc.Mapping`
:param custom_import_extensions: (ignored, for backward compatibility)
:param indented: optional declaration that the string is Sass, not SCSS
                 formatted. :const:`False` by default
:type indented: :class:`bool`
:returns: the compiled CSS string
:param importers: optional callback functions.
                 see also below `importer callbacks
                 <importer-callbacks_>`_ description
:type importers: :class:`collections.abc.Callable`
:rtype: :class:`str`
:raises sass.CompileError: when it fails for any reason
                           (for example the given Sass has broken syntax)

The ``filename`` is the most commonly used way.  It takes a string of
Sass filename, and then returns a compiled CSS string.

:param filename: the filename of Sass source code to compile.
                 it's exclusive to ``string`` and ``dirname`` parameters
:type filename: :class:`str`
:param output_style: an optional coding style of the compiled result.
                     choose one of: ``'nested'`` (default), ``'expanded'``,
                     ``'compact'``, ``'compressed'``
:type output_style: :class:`str`
:param source_comments: whether to add comments about source lines.
                        :const:`False` by default
:type source_comments: :class:`bool`
:param source_map_filename: use source maps and indicate the source map
                            output filename.  :const:`None` means not
                            using source maps.  :const:`None` by default.
:type source_map_filename: :class:`str`
:param source_map_contents: embed include contents in map
:type source_map_contents: :class:`bool`
:param source_map_embed: embed sourceMappingUrl as data URI
:type source_map_embed: :class:`bool`
:param omit_source_map_url: omit source map URL comment from output
:type omit_source_map_url: :class:`bool`
:param source_map_root: base path, will be emitted in source map as is
:type source_map_root: :class:`str`
:param include_paths: an optional list of paths to find ``@import``\\ ed
                      Sass/CSS source files
:type include_paths: :class:`collections.abc.Sequence`
:param precision: optional precision for numbers. :const:`5` by default.
:type precision: :class:`int`
:param custom_functions: optional mapping of custom functions.
                         see also below `custom functions
                         <custom-functions_>`_ description
:type custom_functions: :class:`set`,
                        :class:`collections.abc.Sequence`,
                        :class:`collections.abc.Mapping`
:param custom_import_extensions: (ignored, for backward compatibility)
:param importers: optional callback functions.
                 see also below `importer callbacks
                 <importer-callbacks_>`_ description
:type importers: :class:`collections.abc.Callable`
:returns: the compiled CSS string, or a pair of the compiled CSS string
          and the source map string if ``source_map_filename`` is set
:rtype: :class:`str`, :class:`tuple`
:raises sass.CompileError: when it fails for any reason
                           (for example the given Sass has broken syntax)
:raises exceptions.IOError: when the ``filename`` doesn't exist or
                            cannot be read

The ``dirname`` is useful for automation.  It takes a pair of paths.
The first of the ``dirname`` pair refers the source directory, contains
several Sass source files to compiled.  Sass source files can be nested
in directories.  The second of the pair refers the output directory
that compiled CSS files would be saved.  Directory tree structure of
the source directory will be maintained in the output directory as well.
If ``dirname`` parameter is used the function returns :const:`None`.

:param dirname: a pair of ``(source_dir, output_dir)``.
                it's exclusive to ``string`` and ``filename``
                parameters
:type dirname: :class:`tuple`
:param output_style: an optional coding style of the compiled result.
                     choose one of: ``'nested'`` (default), ``'expanded'``,
                     ``'compact'``, ``'compressed'``
:type output_style: :class:`str`
:param source_comments: whether to add comments about source lines.
                        :const:`False` by default
:type source_comments: :class:`bool`
:param source_map_contents: embed include contents in map
:type source_map_contents: :class:`bool`
:param source_map_embed: embed sourceMappingUrl as data URI
:type source_map_embed: :class:`bool`
:param omit_source_map_url: omit source map URL comment from output
:type omit_source_map_url: :class:`bool`
:param source_map_root: base path, will be emitted in source map as is
:type source_map_root: :class:`str`
:param include_paths: an optional list of paths to find ``@import``\\ ed
                      Sass/CSS source files
:type include_paths: :class:`collections.abc.Sequence`
:param precision: optional precision for numbers. :const:`5` by default.
:type precision: :class:`int`
:param custom_functions: optional mapping of custom functions.
                         see also below `custom functions
                         <custom-functions_>`_ description
:type custom_functions: :class:`set`,
                        :class:`collections.abc.Sequence`,
                        :class:`collections.abc.Mapping`
:param custom_import_extensions: (ignored, for backward compatibility)
:raises sass.CompileError: when it fails for any reason
                           (for example the given Sass has broken syntax)

.. _custom-functions:

The ``custom_functions`` parameter can take three types of forms:

:class:`~set`/:class:`~collections.abc.Sequence` of \\
:class:`SassFunction`\\ s
   It is the most general form.  Although pretty verbose, it can take
   any kind of callables like type objects, unnamed functions,
   and user-defined callables.

   .. code-block:: python

      sass.compile(
          ...,
          custom_functions={
              sass.SassFunction('func-name', ('$a', '$b'), some_callable),
              ...
          }
      )

:class:`~collections.abc.Mapping` of names to functions
   Less general, but easier-to-use form.  Although it's not it can take
   any kind of callables, it can take any kind of *functions* defined
   using :keyword:`def`/:keyword:`lambda` syntax.
   It cannot take callables other than them since inspecting arguments
   is not always available for every kind of callables.

   .. code-block:: python

      sass.compile(
          ...,
          custom_functions={
              'func-name': lambda a, b: ...,
              ...
          }
      )

:class:`~set`/:class:`~collections.abc.Sequence` of \\
named functions
   Not general, but the easiest-to-use form for *named* functions.
   It can take only named functions, defined using :keyword:`def`.
   It cannot take lambdas sinc names are unavailable for them.

   .. code-block:: python

      def func_name(a, b):
          return ...

      sass.compile(
          ...,
          custom_functions={func_name}
      )

.. _importer-callbacks:

Newer versions of ``libsass`` allow developers to define callbacks to be
called and given a chance to process ``@import`` directives. You can
define yours by passing in a list of callables via the ``importers``
parameter. The callables must be passed as 2-tuples in the form:

.. code-block:: python

    (priority_int, callback_fn)

A priority of zero is acceptable; priority determines the order callbacks
are attempted.

These callbacks can accept one or two string arguments. The first argument
is the path that was passed to the ``@import`` directive; the second
(optional) argument is the previous resolved path, where the ``@import``
directive was found. The callbacks must either return ``None`` to
indicate the path wasn't handled by that callback (to continue with others
or fall back on internal ``libsass`` filesystem behaviour) or a list of
one or more tuples, each in one of three forms:

* A 1-tuple representing an alternate path to handle internally; or,
* A 2-tuple representing an alternate path and the content that path
  represents; or,
* A 3-tuple representing the same as the 2-tuple with the addition of a
  "sourcemap".

All tuple return values must be strings. As a not overly realistic
example:

.. code-block:: python

    def my_importer(path, prev):
        return [(path, '#' + path + ' { color: red; }')]

    sass.compile(
            ...,
            importers=[(0, my_importer)]
        )

Now, within the style source, attempting to ``@import 'button';`` will
instead attach ``color: red`` as a property of an element with the
imported name.

.. versionadded:: 0.4.0
   Added ``source_comments`` and ``source_map_filename`` parameters.

.. versionchanged:: 0.6.0
   The ``source_comments`` parameter becomes to take only :class:`bool`
   instead of :class:`str`.

.. deprecated:: 0.6.0
   Values like ``'none'``, ``'line_numbers'``, and ``'map'`` for
   the ``source_comments`` parameter are deprecated.

.. versionadded:: 0.7.0
   Added ``precision`` parameter.

.. versionadded:: 0.7.0
   Added ``custom_functions`` parameter.

.. versionadded:: 0.11.0
   ``source_map_filename`` no longer implies ``source_comments``.

.. versionadded:: 0.17.0
   Added ``source_map_contents``, ``source_map_embed``,
   ``omit_source_map_url``, and ``source_map_root`` parameters.

.. versionadded:: 0.18.0
    The importer callbacks can now take a second argument, the previously-
    resolved path, so that importers can do relative path resolution.

"""

@overload
def compile(
    *,
    filename: str,
    output_style: _OutputStyle = "nested",
    source_comments: bool = False,
    source_map_filename: None = None,
    output_filename_hint: str | None = None,
    source_map_contents: bool = False,
    source_map_embed: bool = False,
    omit_source_map_url: bool = False,
    source_map_root: str | None = None,
    include_paths: Sequence[str] = (),
    precision: int = 5,
    custom_functions: _CustomFunctions = (),
    importers: Iterable[tuple[int, _ImportCallback]] | None = None,
) -> str: ...
@overload
def compile(
    *,
    filename: str,
    output_style: _OutputStyle = "nested",
    source_comments: bool = False,
    source_map_filename: str,
    output_filename_hint: str | None = None,
    source_map_contents: bool = False,
    source_map_embed: bool = False,
    omit_source_map_url: bool = False,
    source_map_root: str | None = None,
    include_paths: Sequence[str] = (),
    precision: int = 5,
    custom_functions: _CustomFunctions = (),
    importers: Iterable[tuple[int, _ImportCallback]] | None = None,
) -> tuple[str, str]: ...
@overload
def compile(
    *,
    dirname: tuple[str, str],
    output_style: _OutputStyle = "nested",
    source_comments: bool = False,
    source_map_contents: bool = False,
    source_map_embed: bool = False,
    omit_source_map_url: bool = False,
    source_map_root: str | None = None,
    include_paths: Sequence[str] = (),
    precision: int = 5,
    custom_functions: _CustomFunctions = (),
    importers: Iterable[tuple[int, _ImportCallback]] | None = None,
) -> None: ...
def and_join(strings: Sequence[str]) -> str:
    """Join the given ``strings`` by commas with last `' and '` conjunction.

    >>> and_join(['Korea', 'Japan', 'China', 'Taiwan'])
    'Korea, Japan, China, and Taiwan'

    :param strings: a list of words to join
    :type string: :class:`collections.abc.Sequence`
    :returns: a joined string
    :rtype: :class:`str`, :class:`basestring`

    """

@type_check_only
class _SassNumber(NamedTuple):
    value: float
    unit: str

class SassNumber(_SassNumber):
    def __new__(cls, value: ConvertibleToFloat, unit: str | bytes) -> Self: ...

@type_check_only
class _SassColor(NamedTuple):
    r: float
    g: float
    b: float
    a: float

class SassColor(_SassColor):
    def __new__(cls, r: ConvertibleToFloat, g: ConvertibleToFloat, b: ConvertibleToFloat, a: ConvertibleToFloat) -> Self: ...

@type_check_only
class _Separator(enum.Enum):
    SASS_SEPARATOR_COMMA = enum.auto()
    SASS_SEPARATOR_SPACE = enum.auto()

SASS_SEPARATOR_COMMA: Literal[_Separator.SASS_SEPARATOR_COMMA]
SASS_SEPARATOR_SPACE: Literal[_Separator.SASS_SEPARATOR_SPACE]

@type_check_only
class _SassList(NamedTuple, Generic[_T]):
    items: tuple[_T, ...]
    separator: _Separator
    bracketed: bool

class SassList(_SassList[_T]):
    def __new__(cls, items: Iterable[_T], separator: _Separator, bracketed: bool = ...) -> SassList[_T]: ...

@type_check_only
class _SassError(NamedTuple):
    msg: str

class SassError(_SassError):
    def __new__(cls, msg: str | bytes) -> Self: ...

@type_check_only
class _SassWarning(NamedTuple):
    msg: str

class SassWarning(_SassWarning):
    def __new__(cls, msg: str | bytes) -> Self: ...

class SassMap(Mapping[_KT, _VT_co]):
    """Because sass maps can have mapping types as keys, we need an immutable
    hashable mapping type.

    .. versionadded:: 0.7.0

    """

    # copied from dict.__init__ in builtins.pyi, since it uses dict() internally
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self: SassMap[str, _VT_co], **kwargs: _VT_co) -> None: ...  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    @overload
    def __init__(self, map: SupportsKeysAndGetItem[_KT, _VT_co], /) -> None: ...
    @overload
    def __init__(
        self: SassMap[str, _VT_co],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        map: SupportsKeysAndGetItem[str, _VT_co],
        /,
        **kwargs: _VT_co,
    ) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[tuple[_KT, _VT_co]], /) -> None: ...
    @overload
    def __init__(
        self: SassMap[str, _VT_co],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        iterable: Iterable[tuple[str, _VT_co]],
        /,
        **kwargs: _VT_co,
    ) -> None: ...
    def __getitem__(self, key: _KT) -> _VT_co: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __len__(self) -> int: ...
    def __hash__(self) -> int: ...

__all__ = (
    "MODES",
    "OUTPUT_STYLES",
    "SOURCE_COMMENTS",
    "CompileError",
    "SassColor",
    "SassError",
    "SassFunction",
    "SassList",
    "SassMap",
    "SassNumber",
    "SassWarning",
    "and_join",
    "compile",
    "libsass_version",
)
