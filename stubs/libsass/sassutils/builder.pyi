""":mod:`sassutils.builder` --- Build the whole directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from collections.abc import Mapping
from re import Pattern
from typing import Any

from sass import _OutputStyle

SUFFIXES: frozenset[str]
SUFFIX_PATTERN: Pattern[str]

def build_directory(
    sass_path: str,
    css_path: str,
    output_style: _OutputStyle = "nested",
    _root_sass: None = None,  # internal arguments for recursion
    _root_css: None = None,  # internal arguments for recursion
    strip_extension: bool = False,
) -> dict[str, str]:
    """Compiles all Sass/SCSS files in ``path`` to CSS.

    :param sass_path: the path of the directory which contains source files
                      to compile
    :type sass_path: :class:`str`, :class:`basestring`
    :param css_path: the path of the directory compiled CSS files will go
    :type css_path: :class:`str`, :class:`basestring`
    :param output_style: an optional coding style of the compiled result.
                         choose one of: ``'nested'`` (default), ``'expanded'``,
                         ``'compact'``, ``'compressed'``
    :type output_style: :class:`str`
    :returns: a dictionary of source filenames to compiled CSS filenames
    :rtype: :class:`collections.abc.Mapping`

    .. versionadded:: 0.6.0
       The ``output_style`` parameter.

    """

class Manifest:
    """Building manifest of Sass/SCSS.

    :param sass_path: the path of the directory that contains Sass/SCSS
                      source files
    :type sass_path: :class:`str`, :class:`basestring`
    :param css_path: the path of the directory to store compiled CSS
                     files
    :type css_path: :class:`str`, :class:`basestring`
    :param strip_extension: whether to remove the original file extension
    :type strip_extension: :class:`bool`
    """

    @classmethod
    def normalize_manifests(
        cls, manifests: Mapping[str, Manifest | tuple[Any, ...] | Mapping[str, Any] | str] | None
    ) -> dict[str, Manifest]: ...
    sass_path: str
    css_path: str
    wsgi_path: str
    strip_extension: bool
    def __init__(
        self, sass_path: str, css_path: str | None = None, wsgi_path: str | None = None, strip_extension: bool | None = None
    ) -> None: ...
    def resolve_filename(self, package_dir: str, filename: str) -> tuple[str, str]:
        """Gets a proper full relative path of Sass source and
        CSS source that will be generated, according to ``package_dir``
        and ``filename``.

        :param package_dir: the path of package directory
        :type package_dir: :class:`str`, :class:`basestring`
        :param filename: the filename of Sass/SCSS source to compile
        :type filename: :class:`str`, :class:`basestring`
        :returns: a pair of (sass, css) path
        :rtype: :class:`tuple`

        """

    def unresolve_filename(self, package_dir: str, filename: str) -> str:
        """Retrieves the probable source path from the output filename.  Pass
        in a .css path to get out a .scss path.

        :param package_dir: the path of the package directory
        :type package_dir: :class:`str`
        :param filename: the css filename
        :type filename: :class:`str`
        :returns: the scss filename
        :rtype: :class:`str`
        """

    def build(self, package_dir: str, output_style: _OutputStyle = "nested") -> frozenset[str]:
        """Builds the Sass/SCSS files in the specified :attr:`sass_path`.
        It finds :attr:`sass_path` and locates :attr:`css_path`
        as relative to the given ``package_dir``.

        :param package_dir: the path of package directory
        :type package_dir: :class:`str`, :class:`basestring`
        :param output_style: an optional coding style of the compiled result.
                             choose one of: ``'nested'`` (default),
                             ``'expanded'``, ``'compact'``, ``'compressed'``
        :type output_style: :class:`str`
        :returns: the set of compiled CSS filenames
        :rtype: :class:`frozenset`

        .. versionadded:: 0.6.0
           The ``output_style`` parameter.

        """

    def build_one(self, package_dir: str, filename: str, source_map: bool = False) -> str:
        """Builds one Sass/SCSS file.

        :param package_dir: the path of package directory
        :type package_dir: :class:`str`, :class:`basestring`
        :param filename: the filename of Sass/SCSS source to compile
        :type filename: :class:`str`, :class:`basestring`
        :param source_map: whether to use source maps.  if :const:`True`
                           it also write a source map to a ``filename``
                           followed by :file:`.map` suffix.
                           default is :const:`False`
        :type source_map: :class:`bool`
        :returns: the filename of compiled CSS
        :rtype: :class:`str`, :class:`basestring`

        .. versionadded:: 0.4.0
           Added optional ``source_map`` parameter.

        """

__all__ = ("SUFFIXES", "SUFFIX_PATTERN", "Manifest", "build_directory")
