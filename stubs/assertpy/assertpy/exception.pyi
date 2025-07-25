from typing import Any
from typing_extensions import Self

__tracebackhide__: bool

class ExceptionMixin:
    """Expected exception mixin."""

    def raises(self, ex: type[BaseException] | BaseException) -> Self:
        """Asserts that val is callable and set the expected exception.

        Just sets the expected exception, but never calls val, and therefore never failes. You must
        chain to :meth:`~when_called_with` to invoke ``val()``.

        Args:
            ex: the expected exception

        Examples:
            Usage::

                assert_that(some_func).raises(RuntimeError).when_called_with('foo')

        Returns:
            AssertionBuilder: returns a new instance (now with the given expected exception) to chain to the next assertion
        """
    # The types of some_args and some_kwargs must equal the types of the called function.
    def when_called_with(self, *some_args: Any, **some_kwargs: Any) -> Self:
        """Asserts that val, when invoked with the given args and kwargs, raises the expected exception.

        Invokes ``val()`` with the given args and kwargs.  You must first set the expected
        exception with :meth:`~raises`.

        Args:
            *some_args: the args to call ``val()``
            **some_kwargs: the kwargs to call ``val()``

        Examples:
            Usage::

                def some_func(a):
                    raise RuntimeError('some error!')

                assert_that(some_func).raises(RuntimeError).when_called_with('foo')

        Returns:
            AssertionBuilder: returns a new instance (now with the captured exception error message as the val) to chain to the next assertion

        Raises:
            AssertionError: if val does **not** raise the expected exception
            TypeError: if expected exception not set via :meth:`raises`
        """
