"""Assertion library for python unit testing with a fluent API"""

import logging
from collections.abc import Callable, Generator
from typing import Any
from typing_extensions import Self

from .base import BaseMixin
from .collection import CollectionMixin
from .contains import ContainsMixin
from .date import DateMixin
from .dict import DictMixin
from .dynamic import DynamicMixin
from .exception import ExceptionMixin
from .extracting import ExtractingMixin
from .file import FileMixin
from .helpers import HelpersMixin
from .numeric import NumericMixin
from .snapshot import SnapshotMixin
from .string import StringMixin

__version__: str
__tracebackhide__: bool

class WarningLoggingAdapter(logging.LoggerAdapter[logging.Logger]):
    """Logging adapter to unwind the stack to get the correct callee filename and line number."""

    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]: ...

class AssertionBuilder(
    StringMixin,
    SnapshotMixin,
    NumericMixin,
    HelpersMixin,
    FileMixin,
    ExtractingMixin,
    ExceptionMixin,
    DynamicMixin,
    DictMixin,
    DateMixin,
    ContainsMixin,
    CollectionMixin,
    BaseMixin,
):
    """The main assertion class.  Never call the constructor directly, always use the
    :meth:`assert_that` helper instead.  Or if you just want warning messages, use the
    :meth:`assert_warn` helper.

    Args:
        val: the value to be tested (aka the actual value)
        description (str, optional): the extra error message description.  Defaults to ``''``
            (aka empty string)
        kind (str, optional): the kind of assertions, one of ``None``, ``soft``, or ``warn``.
            Defaults to ``None``
        expected (Error, optional): the expected exception.  Defaults to ``None``
        logger (Logger, optional): the logger for warning messages.  Defaults to ``None``
    """

    val: Any
    description: str
    kind: str | None
    expected: BaseException | None
    logger: logging.Logger
    def __init__(
        self,
        val: Any,
        description: str = "",
        kind: str | None = None,
        expected: BaseException | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Never call this constructor directly."""

    def builder(
        self,
        val: Any,
        description: str = "",
        kind: str | None = None,
        expected: BaseException | None = None,
        logger: logging.Logger | None = None,
    ) -> Self:
        """Helper to build a new :class:`AssertionBuilder` instance. Use this only if not chaining to ``self``.

        Args:
            val: the value to be tested (aka the actual value)
            description (str, optional): the extra error message description.  Defaults to ``''``
                (aka empty string)
            kind (str, optional): the kind of assertions, one of ``None``, ``soft``, or ``warn``.
                Defaults to ``None``
            expected (Error, optional): the expected exception.  Defaults to ``None``
            logger (Logger, optional): the logger for warning messages.  Defaults to ``None``
        """

    def error(self, msg: str) -> Self:
        """Helper to raise an ``AssertionError`` with the given message.

        If an error description is set by :meth:`~assertpy.base.BaseMixin.described_as`, then that
        description is prepended to the error message.

        Args:
            msg: the error message

        Examples:
            Used to fail an assertion::

                if self.val != other:
                    self.error('Expected <%s> to be equal to <%s>, but was not.' % (self.val, other))

        Raises:
            AssertionError: always raised unless ``kind`` is ``warn`` (as set when using an
                :meth:`assert_warn` assertion) or ``kind`` is ``soft`` (as set when inside a
                :meth:`soft_assertions` context).
        """

def soft_assertions() -> Generator[None, None, None]:
    """Create a soft assertion context.

    Normally, any assertion failure will halt test execution immediately by raising an error.
    Soft assertions are way to collect assertion failures (and failure messages) together, to be
    raised all at once at the end, without halting your test.

    Examples:
        Create a soft assertion context, and some failing tests::

            from assertpy import assert_that, soft_assertions

            with soft_assertions():
                assert_that('foo').is_length(4)
                assert_that('foo').is_empty()
                assert_that('foo').is_false()
                assert_that('foo').is_digit()
                assert_that('123').is_alpha()

        When the context ends, any assertion failures are collected together and a single
        ``AssertionError`` is raised::

            AssertionError: soft assertion failures:
            1. Expected <foo> to be of length <4>, but was <3>.
            2. Expected <foo> to be empty string, but was not.
            3. Expected <False>, but was not.
            4. Expected <foo> to contain only digits, but did not.
            5. Expected <123> to contain only alphabetic chars, but did not.

    Note:
        The soft assertion context only collects *assertion* failures, other errors such as
        ``TypeError`` or ``ValueError`` are always raised immediately.  Triggering an explicit test
        failure with :meth:`fail` will similarly halt execution immediately.  If you need more
        forgiving behavior, use :meth:`soft_fail` to add a failure message without halting test
        execution.
    """

def assert_that(val: Any, description: str = "") -> AssertionBuilder:
    """Set the value to be tested, plus an optional description, and allow assertions to be called.

    This is a factory method for the :class:`AssertionBuilder`, and the single most important
    method in all of assertpy.

    Args:
        val: the value to be tested (aka the actual value)
        description (str, optional): the extra error message description. Defaults to ``''``
            (aka empty string)

    Examples:
        Just import it once at the top of your test file, and away you go...::

            from assertpy import assert_that

            def test_something():
                assert_that(1 + 2).is_equal_to(3)
                assert_that('foobar').is_length(6).starts_with('foo').ends_with('bar')
                assert_that(['a', 'b', 'c']).contains('a').does_not_contain('x')
    """

def assert_warn(val: Any, description: str = "", logger: logging.Logger | None = None) -> AssertionBuilder:
    """Set the value to be tested, and optional description and logger, and allow assertions to be
    called, but never fail, only log warnings.

    This is a factory method for the :class:`AssertionBuilder`, but unlike :meth:`assert_that` an
    `AssertionError` is never raised, and execution is never halted.  Instead, any assertion failures
    results in a warning message being logged. Uses the given logger, or defaults to a simple logger
    that prints warnings to ``stdout``.


    Args:
        val: the value to be tested (aka the actual value)
        description (str, optional): the extra error message description. Defaults to ``''``
            (aka empty string)
        logger (Logger, optional): the logger for warning message on assertion failure. Defaults to ``None``
            (aka use the default simple logger that prints warnings to ``stdout``)

    Examples:
        Usage::

            from assertpy import assert_warn

            assert_warn('foo').is_length(4)
            assert_warn('foo').is_empty()
            assert_warn('foo').is_false()
            assert_warn('foo').is_digit()
            assert_warn('123').is_alpha()

        Even though all of the above assertions fail, ``AssertionError`` is never raised and
        test execution is never halted.  Instead, the failed assertions merely log the following
        warning messages to ``stdout``::

            2019-10-27 20:00:35 WARNING [test_foo.py:23]: Expected <foo> to be of length <4>, but was <3>.
            2019-10-27 20:00:35 WARNING [test_foo.py:24]: Expected <foo> to be empty string, but was not.
            2019-10-27 20:00:35 WARNING [test_foo.py:25]: Expected <False>, but was not.
            2019-10-27 20:00:35 WARNING [test_foo.py:26]: Expected <foo> to contain only digits, but did not.
            2019-10-27 20:00:35 WARNING [test_foo.py:27]: Expected <123> to contain only alphabetic chars, but did not.

    Tip:
        Use :meth:`assert_warn` if and only if you have a *really* good reason to log assertion
        failures instead of failing.
    """

def fail(msg: str = "") -> None:
    """Force immediate test failure with the given message.

    Args:
        msg (str, optional): the failure message.  Defaults to ``''``

    Examples:
        Fail a test::

            from assertpy import assert_that, fail

            def test_fail():
                fail('forced fail!')

        If you wanted to test for a known failure, here is a useful pattern::

            import operator

            def test_adder_bad_arg():
                try:
                    operator.add(1, 'bad arg')
                    fail('should have raised error')
                except TypeError as e:
                    assert_that(str(e)).contains('unsupported operand')
    """

def soft_fail(msg: str = "") -> None:
    """Within a :meth:`soft_assertions` context, append the failure message to the soft error list,
    but do not halt test execution.

    Otherwise, outside the context, acts identical to :meth:`fail` and forces immediate test
    failure with the given message.

    Args:
        msg (str, optional): the failure message.  Defaults to ``''``

    Examples:
        Failing soft assertions::

            from assertpy import assert_that, soft_assertions, soft_fail

            with soft_assertions():
                assert_that(1).is_equal_to(2)
                soft_fail('my message')
                assert_that('foo').is_equal_to('bar')

        Fails, and outputs the following soft error list::

            AssertionError: soft assertion failures:
            1. Expected <1> to be equal to <2>, but was not.
            2. Fail: my message!
            3. Expected <foo> to be equal to <bar>, but was not.

    """

def add_extension(func: Callable[[AssertionBuilder], AssertionBuilder]) -> None:
    """Add a new user-defined custom assertion to assertpy.

    Once the assertion is registered with assertpy, use it like any other assertion.  Pass val to
    :meth:`assert_that`, and then call it.

    Args:
        func: the assertion function (to be added)

    Examples:
        Usage::

            from assertpy import add_extension

            def is_5(self):
                if self.val != 5:
                    self.error(f'{self.val} is NOT 5!')
                return self

            add_extension(is_5)

            def test_5():
                assert_that(5).is_5()

            def test_6():
                assert_that(6).is_5()  # fails
                # 6 is NOT 5!
    """

def remove_extension(func: Callable[[AssertionBuilder], AssertionBuilder]) -> None:
    """Remove a user-defined custom assertion.

    Args:
        func: the assertion function (to be removed)

    Examples:
        Usage::

            from assertpy import remove_extension

            remove_extension(is_5)
    """
