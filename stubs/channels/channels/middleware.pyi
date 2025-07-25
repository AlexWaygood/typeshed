from asgiref.typing import ASGIReceiveCallable, ASGISendCallable

from .consumer import _ChannelScope
from .utils import _ChannelApplication

class BaseMiddleware:
    """
    Base class for implementing ASGI middleware.

    Note that subclasses of this are not self-safe; don't store state on
    the instance, as it serves multiple application instances. Instead, use
    scope.
    """

    inner: _ChannelApplication

    def __init__(self, inner: _ChannelApplication) -> None:
        """
        Middleware constructor - just takes inner application.
        """

    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> _ChannelApplication:
        """
        ASGI application; can insert things into the scope and run asynchronous
        code.
        """
