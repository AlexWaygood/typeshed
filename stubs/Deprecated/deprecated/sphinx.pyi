"""
Sphinx directive integration
============================

We usually need to document the life-cycle of functions and classes:
when they are created, modified or deprecated.

To do that, `Sphinx <http://www.sphinx-doc.org>`_ has a set
of `Paragraph-level markups <http://www.sphinx-doc.org/en/stable/markup/para.html>`_:

- ``versionadded``: to document the version of the project which added the described feature to the library,
- ``versionchanged``: to document changes of a feature,
- ``deprecated``: to document a deprecated feature.

The purpose of this module is to defined decorators which adds this Sphinx directives
to the docstring of your function and classes.

Of course, the ``@deprecated`` decorator will emit a deprecation warning
when the function/method is called or the class is constructed.
"""

from collections.abc import Callable
from typing import Any, Literal, TypeVar

from .classic import ClassicAdapter, _Actions

_F = TypeVar("_F", bound=Callable[..., Any])

class SphinxAdapter(ClassicAdapter):
    """
    Sphinx adapter -- *for advanced usage only*

    This adapter override the :class:`~deprecated.classic.ClassicAdapter`
    in order to add the Sphinx directives to the end of the function/class docstring.
    Such a directive is a `Paragraph-level markup <http://www.sphinx-doc.org/en/stable/markup/para.html>`_

    - The directive can be one of "versionadded", "versionchanged" or "deprecated".
    - The version number is added if provided.
    - The reason message is obviously added in the directive block if not empty.
    """

    directive: Literal["versionadded", "versionchanged", "deprecated"]
    reason: str
    version: str
    action: _Actions | None
    category: type[Warning]
    def __init__(
        self,
        directive: Literal["versionadded", "versionchanged", "deprecated"],
        reason: str = "",
        version: str = "",
        action: _Actions | None = None,
        category: type[Warning] = ...,
        extra_stacklevel: int = 0,
        line_length: int = 70,
    ) -> None:
        """
        Construct a wrapper adapter.

        :type  directive: str
        :param directive:
            Sphinx directive: can be one of "versionadded", "versionchanged" or "deprecated".

        :type  reason: str
        :param reason:
            Reason message which documents the deprecation in your library (can be omitted).

        :type  version: str
        :param version:
            Version of your project which deprecates this feature.
            If you follow the `Semantic Versioning <https://semver.org/>`_,
            the version number has the format "MAJOR.MINOR.PATCH".

        :type  action: Literal["default", "error", "ignore", "always", "module", "once"]
        :param action:
            A warning filter used to activate or not the deprecation warning.
            Can be one of "error", "ignore", "always", "default", "module", or "once".
            If ``None`` or empty, the global filtering mechanism is used.
            See: `The Warnings Filter`_ in the Python documentation.

        :type  category: Type[Warning]
        :param category:
            The warning category to use for the deprecation warning.
            By default, the category class is :class:`~DeprecationWarning`,
            you can inherit this class to define your own deprecation warning category.

        :type  extra_stacklevel: int
        :param extra_stacklevel:
            Number of additional stack levels to consider instrumentation rather than user code.
            With the default value of 0, the warning refers to where the class was instantiated
            or the function was called.

        :type  line_length: int
        :param line_length:
            Max line length of the directive text. If non nul, a long text is wrapped in several lines.

        .. versionchanged:: 1.2.15
            Add the *extra_stacklevel* parameter.
        """

    def __call__(self, wrapped: _F) -> Callable[[_F], _F]:
        """
        Add the Sphinx directive to your class or function.

        :param wrapped: Wrapped class or function.

        :return: the decorated class or function.
        """

def versionadded(reason: str = "", version: str = "", line_length: int = 70) -> Callable[[_F], _F]:
    """
    This decorator can be used to insert a "versionadded" directive
    in your function/class docstring in order to document the
    version of the project which adds this new functionality in your library.

    :param str reason:
        Reason message which documents the addition in your library (can be omitted).

    :param str version:
        Version of your project which adds this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH", and,
        in the case of a new functionality, the "PATCH" component should be "0".

    :type  line_length: int
    :param line_length:
        Max line length of the directive text. If non nul, a long text is wrapped in several lines.

    :return: the decorated function.
    """

def versionchanged(reason: str = "", version: str = "", line_length: int = 70) -> Callable[[_F], _F]:
    """
    This decorator can be used to insert a "versionchanged" directive
    in your function/class docstring in order to document the
    version of the project which modifies this functionality in your library.

    :param str reason:
        Reason message which documents the modification in your library (can be omitted).

    :param str version:
        Version of your project which modifies this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH".

    :type  line_length: int
    :param line_length:
        Max line length of the directive text. If non nul, a long text is wrapped in several lines.

    :return: the decorated function.
    """

def deprecated(
    reason: str = "",
    version: str = "",
    line_length: int = 70,
    *,
    action: _Actions | None = ...,
    category: type[Warning] | None = ...,
    extra_stacklevel: int = 0,
) -> Callable[[_F], _F]:
    """
    This decorator can be used to insert a "deprecated" directive
    in your function/class docstring in order to document the
    version of the project which deprecates this functionality in your library.

    :param str reason:
        Reason message which documents the deprecation in your library (can be omitted).

    :param str version:
        Version of your project which deprecates this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH".

    :type  line_length: int
    :param line_length:
        Max line length of the directive text. If non nul, a long text is wrapped in several lines.

    Keyword arguments can be:

    -   "action":
        A warning filter used to activate or not the deprecation warning.
        Can be one of "error", "ignore", "always", "default", "module", or "once".
        If ``None``, empty or missing, the global filtering mechanism is used.

    -   "category":
        The warning category to use for the deprecation warning.
        By default, the category class is :class:`~DeprecationWarning`,
        you can inherit this class to define your own deprecation warning category.

    -   "extra_stacklevel":
        Number of additional stack levels to consider instrumentation rather than user code.
        With the default value of 0, the warning refers to where the class was instantiated
        or the function was called.


    :return: a decorator used to deprecate a function.

    .. versionchanged:: 1.2.13
       Change the signature of the decorator to reflect the valid use cases.

    .. versionchanged:: 1.2.15
        Add the *extra_stacklevel* parameter.
    """
