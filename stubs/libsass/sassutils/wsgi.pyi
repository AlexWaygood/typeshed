""":mod:`sassutils.wsgi` --- WSGI middleware for development purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from collections.abc import Iterable, Mapping
from typing import Any

from sassutils.builder import Manifest

class SassMiddleware:
    """WSGI middleware for development purpose.  Every time a CSS file has
    requested it finds a matched Sass/SCSS source file and then compiled
    it into CSS.

    It shows syntax errors in three ways:

    Heading comment
        The result CSS includes detailed error message in the heading
        CSS comment e.g.:

        .. code-block:: css

            /*
            Error: invalid property name
            */

    Red text in ``body:before``
        The result CSS draws detailed error message in ``:before``
        pseudo-class of ``body`` element e.g.:

        .. code-block:: css

            body:before {
                content: 'Error: invalid property name';
                color: maroon;
                background-color: white;
            }

        In most cases you could be aware of syntax error by refreshing your
        working document because it will removes all other styles and leaves
        only a red text.

    :mod:`logging`
        It logs syntax errors if exist during compilation to
        ``sassutils.wsgi.SassMiddleware`` logger with level ``ERROR``.

        To enable this::

            from logging import Formatter, StreamHandler, getLogger
            logger = getLogger('sassutils.wsgi.SassMiddleware')
            handler = StreamHandler(level=logging.ERROR)
            formatter = Formatter(fmt='*' * 80 + '\\n%(message)s\\n' + '*' * 80)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        Or simply::

            import logging
            logging.basicConfig()

    :param app: the WSGI application to wrap
    :type app: :class:`collections.abc.Callable`
    :param manifests: build settings.  the same format to
                      :file:`setup.py` script's ``sass_manifests``
                      option
    :type manifests: :class:`collections.abc.Mapping`
    :param package_dir: optional mapping of package names to directories.
                        the same format to :file:`setup.py` script's
                        ``package_dir`` option
    :type package_dir: :class:`collections.abc.Mapping`

    .. versionchanged:: 0.4.0
       It creates also source map files with filenames followed by
       :file:`.map` suffix.

    .. versionadded:: 0.8.0
       It logs syntax errors if exist during compilation to
       ``sassutils.wsgi.SassMiddleware`` logger with level ``ERROR``.

    """

    app: WSGIApplication
    manifests: dict[str, Manifest]
    error_status: str
    package_dir: Mapping[str, str]
    paths: list[tuple[str, str, Manifest]]
    def __init__(
        self,
        app: WSGIApplication,
        manifests: Mapping[str, Manifest | tuple[Any, ...] | Mapping[str, Any] | str] | None,
        package_dir: Mapping[str, str] = {},
        error_status: str = "200 OK",
    ) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...
    @staticmethod
    def quote_css_string(s: str) -> str:
        """Quotes a string as CSS string literal."""

__all__ = ("SassMiddleware",)
