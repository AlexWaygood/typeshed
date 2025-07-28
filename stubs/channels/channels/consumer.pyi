from collections.abc import Awaitable
from typing import Any, ClassVar, Protocol, TypedDict, type_check_only

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, Scope, WebSocketScope
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.layers import BaseChannelLayer
from django.contrib.sessions.backends.base import SessionBase
from django.utils.functional import LazyObject

# _LazySession is a LazyObject that wraps a SessionBase instance.
# We subclass both for type checking purposes to expose SessionBase attributes,
# and suppress mypy's "misc" error with `# type: ignore[misc]`.
@type_check_only
class _LazySession(SessionBase, LazyObject):  # type: ignore[misc]
    _wrapped: SessionBase

@type_check_only
class _URLRoute(TypedDict):
    # Values extracted from Django's URLPattern matching,
    # passed through ASGI scope routing.
    # `args` and `kwargs` are the result of pattern matching against the URL path.
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

# Channel Scope definition
@type_check_only
class _ChannelScope(WebSocketScope, total=False):
    # Channels specific
    channel: str
    url_route: _URLRoute
    path_remaining: str

    # Auth specific
    cookies: dict[str, str]
    session: _LazySession
    user: UserLazyObject | None

# Accepts any ASGI message dict with a required "type" key (str),
# but allows additional arbitrary keys for flexibility.
def get_handler_name(message: dict[str, Any]) -> str:
    """
    Looks at a message, checks it has a sensible type, and returns the
    handler name for that type.
    """

@type_check_only
class _ASGIApplicationProtocol(Protocol):
    consumer_class: AsyncConsumer

    # Accepts any initialization kwargs passed to the consumer class.
    # Typed as `Any` to allow flexibility in subclass-specific arguments.
    consumer_initkwargs: Any

    def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> Awaitable[None]: ...

class AsyncConsumer:
    """
    Base consumer class. Implements the ASGI application spec, and adds on
    channel layer management and routing of events to named methods based
    on their type.
    """

    channel_layer_alias: ClassVar[str]

    scope: _ChannelScope
    channel_layer: BaseChannelLayer
    channel_name: str
    channel_receive: ASGIReceiveCallable
    base_send: ASGISendCallable

    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        """
        Dispatches incoming messages to type-based handlers asynchronously.
        """

    async def dispatch(self, message: dict[str, Any]) -> None:
        """
        Works out what to do with a message.
        """

    async def send(self, message: dict[str, Any]) -> None:
        """
        Overrideable/callable-by-subclasses send method.
        """
    # initkwargs will be used to instantiate the consumer instance.
    @classmethod
    def as_asgi(cls, **initkwargs: Any) -> _ASGIApplicationProtocol:
        """
        Return an ASGI v3 single callable that instantiates a consumer instance
        per scope. Similar in purpose to Django's as_view().

        initkwargs will be used to instantiate the consumer instance.
        """

class SyncConsumer(AsyncConsumer):
    """
    Synchronous version of the consumer, which is what we write most of the
    generic consumers against (for now). Calls handlers in a threadpool and
    uses CallBouncer to get the send method out to the main event loop.

    It would have been possible to have "mixed" consumers and auto-detect
    if a handler was awaitable or not, but that would have made the API
    for user-called methods very confusing as there'd be two types of each.
    """

    # Since we're overriding asynchronous methods with synchronous ones,
    # we need to use `# type: ignore[override]` to suppress mypy errors.
    @database_sync_to_async
    def dispatch(self, message: dict[str, Any]) -> None:  # type: ignore[override]
        """
        Dispatches incoming messages to type-based handlers asynchronously.
        """

    def send(self, message: dict[str, Any]) -> None:  # type: ignore[override]
        """
        Overrideable/callable-by-subclasses send method.
        """
