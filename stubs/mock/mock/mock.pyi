from _typeshed import Incomplete
from collections.abc import Callable, Coroutine, Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, ClassVar, Generic, Literal, TypeVar, overload
from typing_extensions import ParamSpec, Self

_F = TypeVar("_F", bound=Callable[..., Any])
_AF = TypeVar("_AF", bound=Callable[..., Coroutine[Any, Any, Any]])
_T = TypeVar("_T")
_TT = TypeVar("_TT", bound=type[Any])
_R = TypeVar("_R")
_P = ParamSpec("_P")

__all__ = (
    "Mock",
    "MagicMock",
    "patch",
    "sentinel",
    "DEFAULT",
    "ANY",
    "call",
    "create_autospec",
    "AsyncMock",
    "ThreadingMock",
    "FILTER_DIR",
    "NonCallableMock",
    "NonCallableMagicMock",
    "mock_open",
    "PropertyMock",
    "seal",
)

class InvalidSpecError(Exception):
    """Indicates that an invalid value was used as a mock spec."""

FILTER_DIR: bool

class _SentinelObject:
    """A unique, named, sentinel object."""

    def __init__(self, name: str) -> None: ...
    name: str

class _Sentinel:
    """Access attributes to return a named object, usable as a sentinel."""

    def __getattr__(self, name: str) -> _SentinelObject: ...

sentinel: _Sentinel
DEFAULT: _SentinelObject

class _Call(tuple[Any, ...]):
    """
    A tuple for holding the results of a call to a mock, either in the form
    `(args, kwargs)` or `(name, args, kwargs)`.

    If args or kwargs are empty then a call tuple will compare equal to
    a tuple without those values. This makes comparisons less verbose::

        _Call(('name', (), {})) == ('name',)
        _Call(('name', (1,), {})) == ('name', (1,))
        _Call(((), {'a': 'b'})) == ({'a': 'b'},)

    The `_Call` object provides a useful shortcut for comparing with call::

        _Call(((1, 2), {'a': 3})) == call(1, 2, a=3)
        _Call(('foo', (1, 2), {'a': 3})) == call.foo(1, 2, a=3)

    If the _Call has no name then it will match any name.
    """

    def __new__(
        cls, value: Any = (), name: Incomplete | None = "", parent=None, two: bool = False, from_kall: bool = True
    ) -> Self: ...
    name: Any
    parent: Any
    from_kall: Any
    def __init__(self, value: Any = (), name=None, parent=None, two: bool = False, from_kall: bool = True) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object, /) -> bool: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _Call: ...
    def __getattr__(self, attr: str) -> Any: ...
    @property
    def args(self) -> tuple[Any, ...]: ...
    @property
    def kwargs(self) -> dict[str, Any]: ...
    def call_list(self) -> _CallList:
        """For a call object that represents multiple calls, `call_list`
        returns a list of all the intermediate calls as well as the
        final call.
        """

call: _Call

class _CallList(list[_Call]):
    def __contains__(self, value: Any) -> bool: ...

class Base:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

# We subclass with "Any" because mocks are explicitly designed to stand in for other types,
# something that can't be expressed with our static type system.
class NonCallableMock(Base, Any):
    """A non-callable version of `Mock`"""

    def __new__(
        cls,
        spec: list[str] | object | type[object] | None = None,
        wraps: Any | None = None,
        name: str | None = None,
        spec_set: list[str] | object | type[object] | None = None,
        parent: NonCallableMock | None = None,
        _spec_state=None,
        _new_name: str = "",
        _new_parent: NonCallableMock | None = None,
        _spec_as_instance: bool = False,
        _eat_self: bool | None = None,
        unsafe: bool = False,
        **kwargs: Any,
    ) -> Self: ...
    def __init__(
        self,
        spec: list[str] | object | type[object] | None = None,
        wraps: Any | None = None,
        name: str | None = None,
        spec_set: list[str] | object | type[object] | None = None,
        parent: NonCallableMock | None = None,
        _spec_state=None,
        _new_name: str = "",
        _new_parent: NonCallableMock | None = None,
        _spec_as_instance: bool = False,
        _eat_self: bool | None = None,
        unsafe: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def _calls_repr(self) -> str:
        """Renders self.mock_calls as a string.

                Example: "
        Calls: [call(1), call(2)]."

                If self.mock_calls is empty, an empty string is returned. The
                output will be truncated if very long.
        """

    def assert_called_with(_mock_self, *args: Any, **kwargs: Any) -> None:
        """assert that the last call was made with the specified arguments.

        Raises an AssertionError if the args and keyword args passed in are
        different to the last call to the mock.
        """

    def assert_not_called(_mock_self) -> None:
        """assert that the mock was never called."""

    def assert_called_once_with(_mock_self, *args: Any, **kwargs: Any) -> None:
        """assert that the mock was called exactly once and that that call was
        with the specified arguments.
        """

    def _format_mock_failure_message(self, args: Any, kwargs: Any, action: str = "call") -> str: ...
    def assert_called(_mock_self) -> None:
        """assert that the mock was called at least once"""

    def assert_called_once(_mock_self) -> None:
        """assert that the mock was called only once."""

    def reset_mock(self, visited: Any = None, *, return_value: bool = False, side_effect: bool = False) -> None:
        """Restore the mock object to its initial state."""

    def _extract_mock_name(self) -> str: ...
    def assert_any_call(self, *args: Any, **kwargs: Any) -> None:
        """assert the mock has been called with the specified arguments.

        The assert passes if the mock has *ever* been called, unlike
        `assert_called_with` and `assert_called_once_with` that only pass if
        the call is the most recent one.
        """

    def assert_has_calls(self, calls: Sequence[_Call], any_order: bool = False) -> None:
        """assert the mock has been called with the specified calls.
        The `mock_calls` list is checked for the calls.

        If `any_order` is False (the default) then the calls must be
        sequential. There can be extra calls before or after the
        specified calls.

        If `any_order` is True then the calls can be in any order, but
        they must all appear in `mock_calls`.
        """

    def mock_add_spec(self, spec: Any, spec_set: bool = False) -> None:
        """Add a spec to a mock. `spec` can either be an object or a
        list of strings. Only attributes on the `spec` can be fetched as
        attributes from the mock.

        If `spec_set` is True then only attributes on the spec can be set.
        """

    def _mock_add_spec(self, spec: Any, spec_set: bool, _spec_as_instance: bool = False, _eat_self: bool = False) -> None: ...
    def attach_mock(self, mock: NonCallableMock, attribute: str) -> None:
        """
        Attach a mock as an attribute of this one, replacing its name and
        parent. Calls to the attached mock will be recorded in the
        `method_calls` and `mock_calls` attributes of this one.
        """

    def configure_mock(self, **kwargs: Any) -> None:
        """Set attributes on the mock through keyword arguments.

        Attributes plus return values and side effects can be set on child
        mocks using standard dot notation and unpacking a dictionary in the
        method call:

        >>> attrs = {'method.return_value': 3, 'other.side_effect': KeyError}
        >>> mock.configure_mock(**attrs)
        """
    return_value: Any
    side_effect: Any
    called: bool
    call_count: int
    call_args: Any
    call_args_list: _CallList
    mock_calls: _CallList
    def _format_mock_call_signature(self, args: Any, kwargs: Any) -> str: ...
    def _call_matcher(self, _call: tuple[_Call, ...]) -> _Call:
        """
        Given a call (or simply an (args, kwargs) tuple), return a
        comparison key suitable for matching with other calls.
        This is a best effort method which relies on the spec's signature,
        if available, or falls back on the arguments themselves.
        """

    def _get_child_mock(self, **kw: Any) -> NonCallableMock:
        """Create the child mocks for attributes and return value.
        By default child mocks will be the same type as the parent.
        Subclasses of Mock may want to override this to customize the way
        child mocks are made.

        For non-callable mocks the callable variant will be used (rather than
        any custom subclass).
        """

class CallableMixin(Base):
    side_effect: Any
    def __init__(
        self,
        spec=None,
        side_effect=None,
        return_value: Any = ...,
        wraps=None,
        name=None,
        spec_set=None,
        parent=None,
        _spec_state=None,
        _new_name: Any = "",
        _new_parent=None,
        **kwargs: Any,
    ) -> None: ...
    def __call__(_mock_self, *args: Any, **kwargs: Any) -> Any: ...

class Mock(CallableMixin, NonCallableMock):
    """
    Create a new `Mock` object. `Mock` takes several optional arguments
    that specify the behaviour of the Mock object:

    * `spec`: This can be either a list of strings or an existing object (a
      class or instance) that acts as the specification for the mock object. If
      you pass in an object then a list of strings is formed by calling dir on
      the object (excluding unsupported magic attributes and methods). Accessing
      any attribute not in this list will raise an `AttributeError`.

      If `spec` is an object (rather than a list of strings) then
      `mock.__class__` returns the class of the spec object. This allows mocks
      to pass `isinstance` tests.

    * `spec_set`: A stricter variant of `spec`. If used, attempting to *set*
      or get an attribute on the mock that isn't on the object passed as
      `spec_set` will raise an `AttributeError`.

    * `side_effect`: A function to be called whenever the Mock is called. See
      the `side_effect` attribute. Useful for raising exceptions or
      dynamically changing return values. The function is called with the same
      arguments as the mock, and unless it returns `DEFAULT`, the return
      value of this function is used as the return value.

      If `side_effect` is an iterable then each call to the mock will return
      the next value from the iterable. If any of the members of the iterable
      are exceptions they will be raised instead of returned.

    * `return_value`: The value returned when the mock is called. By default
      this is a new Mock (created on first access). See the
      `return_value` attribute.

    * `unsafe`: By default, accessing any attribute whose name starts with
      *assert*, *assret*, *asert*, *aseert*, or *assrt* raises an AttributeError.
      Additionally, an AttributeError is raised when accessing
      attributes that match the name of an assertion method without the prefix
      `assert_`, e.g. accessing `called_once` instead of `assert_called_once`.
      Passing `unsafe=True` will allow access to these attributes.

    * `wraps`: Item for the mock object to wrap. If `wraps` is not None then
      calling the Mock will pass the call through to the wrapped object
      (returning the real result). Attribute access on the mock will return a
      Mock object that wraps the corresponding attribute of the wrapped object
      (so attempting to access an attribute that doesn't exist will raise an
      `AttributeError`).

      If the mock has an explicit `return_value` set then calls are not passed
      to the wrapped object and the `return_value` is returned instead.

    * `name`: If the mock has a name then it will be used in the repr of the
      mock. This can be useful for debugging. The name is propagated to child
      mocks.

    Mocks can also be called with arbitrary keyword arguments. These will be
    used to set attributes on the mock after it is created.
    """

class _patch(Generic[_T]):
    attribute_name: Any
    getter: Callable[[], Any]
    attribute: str
    new: _T
    new_callable: Any
    spec: Any
    create: bool
    has_local: Any
    spec_set: Any
    autospec: Any
    kwargs: Mapping[str, Any]
    additional_patchers: Any
    def __init__(
        self: _patch[_T],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        getter: Callable[[], Any],
        attribute: str,
        new: _T,
        spec: Incomplete | None,
        create: bool,
        spec_set: Incomplete | None,
        autospec: Incomplete | None,
        new_callable: Incomplete | None,
        kwargs: Mapping[str, Any],
        *,
        unsafe: bool = False,
    ) -> None: ...
    def copy(self) -> _patch[_T]: ...
    def __call__(self, func: Callable[_P, _R]) -> Callable[_P, _R]: ...
    def decorate_class(self, klass: _TT) -> _TT: ...
    def decorate_callable(self, func: _F) -> _F: ...
    def decorate_async_callable(self, func: _AF) -> _AF: ...
    def decoration_helper(
        self, patched: Any, args: tuple[Any, ...], keywargs: dict[str, Any]
    ) -> AbstractContextManager[tuple[tuple[Any, ...], dict[str, Any]]]: ...
    def get_original(self) -> tuple[Any, bool]: ...
    target: Any
    temp_original: Any
    is_local: bool
    def __enter__(self) -> _T:
        """Perform the patch."""

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None, /
    ) -> None:
        """Undo the patch."""

    def start(self) -> _T:
        """Activate a patch, returning any created mock."""

    def stop(self) -> None:
        """Stop an active patch."""

class _patch_dict:
    """
    Patch a dictionary, or dictionary like object, and restore the dictionary
    to its original state after the test, where the restored dictionary is
    a copy of the dictionary as it was before the test.

    `in_dict` can be a dictionary or a mapping like container. If it is a
    mapping then it must at least support getting, setting and deleting items
    plus iterating over keys.

    `in_dict` can also be a string specifying the name of the dictionary, which
    will then be fetched by importing it.

    `values` can be a dictionary of values to set in the dictionary. `values`
    can also be an iterable of `(key, value)` pairs.

    If `clear` is True then the dictionary will be cleared before the new
    values are set.

    `patch.dict` can also be called with arbitrary keyword arguments to set
    values in the dictionary::

        with patch.dict('sys.modules', mymodule=Mock(), other_module=Mock()):
            ...

    `patch.dict` can be used as a context manager, decorator or class
    decorator. When used as a class decorator `patch.dict` honours
    `patch.TEST_PREFIX` for choosing which methods to wrap.
    """

    in_dict: Any
    values: Any
    clear: Any
    def __init__(self, in_dict: Any, values: Any = (), clear: Any = False, **kwargs: Any) -> None: ...
    def __call__(self, f: Any) -> Any: ...
    def decorate_callable(self, f: _F) -> _F: ...
    def decorate_async_callable(self, f: _AF) -> _AF: ...
    def decorate_class(self, klass: Any) -> Any: ...
    def __enter__(self) -> Any:
        """Patch the dict."""

    def __exit__(self, *args: object) -> Any:
        """Unpatch the dict."""
    start: Any
    stop: Any

class _patcher:
    TEST_PREFIX: str
    dict: type[_patch_dict]
    @overload
    def __call__(
        self,
        target: Any,
        *,
        spec: Incomplete | None = ...,
        create: bool = ...,
        spec_set: Incomplete | None = ...,
        autospec: Incomplete | None = ...,
        new_callable: Incomplete | None = ...,
        unsafe: bool = ...,
        **kwargs: Any,
    ) -> _patch[MagicMock | AsyncMock]: ...
    # This overload also covers the case, where new==DEFAULT. In this case, the return type is _patch[Any].
    # Ideally we'd be able to add an overload for it so that the return type is _patch[MagicMock],
    # but that's impossible with the current type system.
    @overload
    def __call__(
        self,
        target: Any,
        new: _T,
        spec: Incomplete | None = ...,
        create: bool = ...,
        spec_set: Incomplete | None = ...,
        autospec: Incomplete | None = ...,
        new_callable: Incomplete | None = ...,
        *,
        unsafe: bool = ...,
        **kwargs: Any,
    ) -> _patch[_T]: ...
    @overload
    def object(
        self,
        target: Any,
        attribute: str,
        *,
        spec: Incomplete | None = ...,
        create: bool = ...,
        spec_set: Incomplete | None = ...,
        autospec: Incomplete | None = ...,
        new_callable: Incomplete | None = ...,
        unsafe: bool = ...,
        **kwargs: Any,
    ) -> _patch[MagicMock | AsyncMock]: ...
    @overload
    def object(
        self,
        target: Any,
        attribute: str,
        new: _T,
        spec: Incomplete | None = ...,
        create: bool = ...,
        spec_set: Incomplete | None = ...,
        autospec: Incomplete | None = ...,
        new_callable: Incomplete | None = ...,
        *,
        unsafe: bool = ...,
        **kwargs: Any,
    ) -> _patch[_T]: ...
    def multiple(
        self,
        target: Any,
        spec: Incomplete | None = ...,
        create: bool = ...,
        spec_set: Incomplete | None = ...,
        autospec: Incomplete | None = ...,
        new_callable: Incomplete | None = ...,
        *,
        unsafe: bool = ...,
        **kwargs: _T,
    ) -> _patch[_T]: ...
    def stopall(self) -> None: ...

patch: _patcher

class MagicMixin:
    def __init__(self, *args: Any, **kw: Any) -> None: ...

class NonCallableMagicMock(MagicMixin, NonCallableMock):
    """A version of `MagicMock` that isn't callable."""

    def mock_add_spec(self, spec: Any, spec_set: bool = False) -> None:
        """Add a spec to a mock. `spec` can either be an object or a
        list of strings. Only attributes on the `spec` can be fetched as
        attributes from the mock.

        If `spec_set` is True then only attributes on the spec can be set.
        """

class MagicMock(MagicMixin, Mock):
    """
    MagicMock is a subclass of Mock with default implementations
    of most of the magic methods. You can use MagicMock without having to
    configure the magic methods yourself.

    If you use the `spec` or `spec_set` arguments then *only* magic
    methods that exist in the spec will be created.

    Attributes and the return value of a `MagicMock` will also be `MagicMocks`.
    """

    def mock_add_spec(self, spec: Any, spec_set: bool = False) -> None:
        """Add a spec to a mock. `spec` can either be an object or a
        list of strings. Only attributes on the `spec` can be fetched as
        attributes from the mock.

        If `spec_set` is True then only attributes on the spec can be set.
        """

class AsyncMockMixin(Base):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def assert_awaited(_mock_self) -> None:
        """
        Assert that the mock was awaited at least once.
        """

    def assert_awaited_once(_mock_self) -> None:
        """
        Assert that the mock was awaited exactly once.
        """

    def assert_awaited_with(_mock_self, *args: Any, **kwargs: Any) -> None:
        """
        Assert that the last await was with the specified arguments.
        """

    def assert_awaited_once_with(_mock_self, *args: Any, **kwargs: Any) -> None:
        """
        Assert that the mock was awaited exactly once and with the specified
        arguments.
        """

    def assert_any_await(_mock_self, *args: Any, **kwargs: Any) -> None:
        """
        Assert the mock has ever been awaited with the specified arguments.
        """

    def assert_has_awaits(_mock_self, calls: Iterable[_Call], any_order: bool = False) -> None:
        """
        Assert the mock has been awaited with the specified calls.
        The :attr:`await_args_list` list is checked for the awaits.

        If `any_order` is False (the default) then the awaits must be
        sequential. There can be extra calls before or after the
        specified awaits.

        If `any_order` is True then the awaits can be in any order, but
        they must all appear in :attr:`await_args_list`.
        """

    def assert_not_awaited(_mock_self) -> None:
        """
        Assert that the mock was never awaited.
        """

    def reset_mock(self, *args: Any, **kwargs: Any) -> None:
        """
        See :func:`.Mock.reset_mock()`
        """
    await_count: int
    await_args: _Call | None
    await_args_list: _CallList
    __name__: str
    __defaults__: tuple[Any, ...]
    __kwdefaults__: dict[str, Any]
    __annotations__: dict[str, Any] | None  # type: ignore[assignment]

class AsyncMagicMixin(MagicMixin): ...

class AsyncMock(AsyncMockMixin, AsyncMagicMixin, Mock):
    """
    Enhance :class:`Mock` with features allowing to mock
    an async function.

    The :class:`AsyncMock` object will behave so the object is
    recognized as an async function, and the result of a call is an awaitable:

    >>> mock = AsyncMock()
    >>> iscoroutinefunction(mock)
    True
    >>> inspect.isawaitable(mock())
    True


    The result of ``mock()`` is an async function which will have the outcome
    of ``side_effect`` or ``return_value``:

    - if ``side_effect`` is a function, the async function will return the
      result of that function,
    - if ``side_effect`` is an exception, the async function will raise the
      exception,
    - if ``side_effect`` is an iterable, the async function will return the
      next value of the iterable, however, if the sequence of result is
      exhausted, ``StopIteration`` is raised immediately,
    - if ``side_effect`` is not defined, the async function will return the
      value defined by ``return_value``, hence, by default, the async function
      returns a new :class:`AsyncMock` object.

    If the outcome of ``side_effect`` or ``return_value`` is an async function,
    the mock async function obtained when the mock object is called will be this
    async function itself (and not an async function returning an async
    function).

    The test author can also specify a wrapped object with ``wraps``. In this
    case, the :class:`Mock` object behavior is the same as with an
    :class:`.Mock` object: the wrapped object may have methods
    defined as async function functions.

    Based on Martin Richard's asynctest project.
    """

    # Improving the `reset_mock` signature.
    # It is defined on `AsyncMockMixin` with `*args, **kwargs`, which is not ideal.
    # But, `NonCallableMock` super-class has the better version.
    def reset_mock(self, visited: Any = None, *, return_value: bool = False, side_effect: bool = False) -> None:
        """
        See :func:`.Mock.reset_mock()`
        """

class MagicProxy(Base):
    name: str
    parent: Any
    def __init__(self, name: str, parent: Any) -> None: ...
    def create_mock(self) -> Any: ...
    def __get__(self, obj: Any, _type=None) -> Any: ...

class _ANY:
    """A helper object that compares equal to everything."""

    def __eq__(self, other: object) -> Literal[True]: ...
    def __ne__(self, other: object) -> Literal[False]: ...

ANY: Any

def create_autospec(
    spec: Any, spec_set: Any = False, instance: Any = False, _parent=None, _name=None, *, unsafe: bool = False, **kwargs: Any
) -> Any:
    """Create a mock object using another object as a spec. Attributes on the
    mock will use the corresponding attribute on the `spec` object as their
    spec.

    Functions or methods being mocked will have their arguments checked
    to check that they are called with the correct signature.

    If `spec_set` is True then attempting to set attributes that don't exist
    on the spec object will raise an `AttributeError`.

    If a class is used as a spec then the return value of the mock (the
    instance of the class) will have the same spec. You can use a class as the
    spec for an instance object by passing `instance=True`. The returned mock
    will only be callable if instances of the mock are callable.

    `create_autospec` will raise a `RuntimeError` if passed some common
    misspellings of the arguments autospec and spec_set. Pass the argument
    `unsafe` with the value True to disable that check.

    `create_autospec` also takes arbitrary keyword arguments that are passed to
    the constructor of the created mock.
    """

class _SpecState:
    spec: Any
    ids: Any
    spec_set: Any
    parent: Any
    instance: Any
    name: Any
    def __init__(self, spec: Any, spec_set: Any = False, parent=None, name=None, ids=None, instance: Any = False) -> None: ...

def mock_open(mock=None, read_data: Any = "") -> Any:
    """
    A helper function to create a mock to replace the use of `open`. It works
    for `open` called directly or used as a context manager.

    The `mock` argument is the mock object to configure. If `None` (the
    default) then a `MagicMock` will be created for you, with the API limited
    to methods or attributes available on standard file handles.

    `read_data` is a string for the `read`, `readline` and `readlines` of the
    file handle to return.  This is an empty string by default.
    """

class PropertyMock(Mock):
    """
    A mock intended to be used as a property, or other descriptor, on a class.
    `PropertyMock` provides `__get__` and `__set__` methods so you can specify
    a return value when it is fetched.

    Fetching a `PropertyMock` instance from an object calls the mock, with
    no args. Setting it calls the mock with the value being set.
    """

    def __get__(self, obj: _T, obj_type: type[_T] | None = None) -> Self: ...
    def __set__(self, obj: Any, value: Any) -> None: ...

def seal(mock: Any) -> None:
    """Disable the automatic generation of child mocks.

    Given an input Mock, seals it to ensure no further mocks will be generated
    when accessing an attribute that was not already defined.

    The operation recursively seals the mock passed in, meaning that
    the mock itself, any mocks generated by accessing one of its attributes,
    and all assigned mocks without a name or spec will be sealed.
    """

class ThreadingMixin(Base):
    DEFAULT_TIMEOUT: ClassVar[float | None]

    def __init__(self, *args: Any, timeout: float | None = ..., **kwargs: Any) -> None: ...
    def reset_mock(self, *args: Any, **kwargs: Any) -> None:
        """
        See :func:`.Mock.reset_mock()`
        """

    def wait_until_called(self, *, timeout: float | None = ...) -> None:
        """Wait until the mock object is called.

        `timeout` - time to wait for in seconds, waits forever otherwise.
        Defaults to the constructor provided timeout.
        Use None to block undefinetively.
        """

    def wait_until_any_call_with(self, *args: Any, **kwargs: Any) -> None:
        """Wait until the mock object is called with given args.

        Waits for the timeout in seconds provided in the constructor.
        """

class ThreadingMock(ThreadingMixin, MagicMixin, Mock):
    """
    A mock that can be used to wait until on calls happening
    in a different thread.

    The constructor can take a `timeout` argument which
    controls the timeout in seconds for all `wait` calls of the mock.

    You can change the default timeout of all instances via the
    `ThreadingMock.DEFAULT_TIMEOUT` attribute.

    If no timeout is set, it will block undefinetively.
    """

    # Improving the `reset_mock` signature.
    # It is defined on `ThreadingMixin` with `*args, **kwargs`, which is not ideal.
    # But, `NonCallableMock` super-class has the better version.
    def reset_mock(self, visited: Any = None, *, return_value: bool = False, side_effect: bool = False) -> None:
        """
        See :func:`.Mock.reset_mock()`
        """
