import datetime
from collections.abc import Awaitable
from typing import Any

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable
from channels.consumer import _ChannelScope
from channels.utils import _ChannelApplication
from django.contrib.sessions.backends.base import SessionBase

class CookieMiddleware:
    """
    Extracts cookies from HTTP or WebSocket-style scopes and adds them as a
    scope["cookies"] entry with the same format as Django's request.COOKIES.
    """

    inner: _ChannelApplication

    def __init__(self, inner: _ChannelApplication) -> None: ...

    # Returns the same type as the provided _ChannelApplication.
    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> Any: ...
    @classmethod
    def set_cookie(
        cls,
        message: dict[str, Any],
        key: str,
        value: str = "",
        max_age: int | None = None,
        expires: str | datetime.datetime | None = None,
        path: str = "/",
        domain: str | None = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str = "lax",
    ) -> None:
        """
        Sets a cookie in the passed HTTP response message.

        ``expires`` can be:
        - a string in the correct format,
        - a naive ``datetime.datetime`` object in UTC,
        - an aware ``datetime.datetime`` object in any time zone.
        If it is a ``datetime.datetime`` object then ``max_age`` will be calculated.
        """

    @classmethod
    def delete_cookie(cls, message: dict[str, Any], key: str, path: str = "/", domain: str | None = None) -> None:
        """
        Deletes a cookie in a response.
        """

class InstanceSessionWrapper:
    """
    Populates the session in application instance scope, and wraps send to save
    the session.
    """

    save_message_types: list[str]
    cookie_response_message_types: list[str]
    cookie_name: str
    session_store: SessionBase
    scope: _ChannelScope
    activated: bool
    real_send: ASGISendCallable

    def __init__(self, scope: _ChannelScope, send: ASGISendCallable) -> None: ...
    async def resolve_session(self) -> None: ...
    async def send(self, message: dict[str, Any]) -> Awaitable[None]:
        """
        Overridden send that also does session saves/cookies.
        """

    async def save_session(self) -> None:
        """
        Saves the current session.
        """

class SessionMiddleware:
    """
    Class that adds Django sessions (from HTTP cookies) to the
    scope. Works with HTTP or WebSocket protocol types (or anything that
    provides a "headers" entry in the scope).

    Requires the CookieMiddleware to be higher up in the stack.
    """

    inner: _ChannelApplication

    def __init__(self, inner: _ChannelApplication) -> None: ...
    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> _ChannelApplication:
        """
        Instantiate a session wrapper for this scope, resolve the session and
        call the inner application.
        """

def SessionMiddlewareStack(inner: _ChannelApplication) -> _ChannelApplication: ...
