from typing import Any, type_check_only

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, Scope
from django.urls.resolvers import URLPattern

from .consumer import _ASGIApplicationProtocol, _ChannelScope
from .utils import _ChannelApplication

def get_default_application() -> ProtocolTypeRouter:
    """
    Gets the default application, set in the ASGI_APPLICATION setting.
    """

class ProtocolTypeRouter:
    """
    Takes a mapping of protocol type names to other Application instances,
    and dispatches to the right one based on protocol name (or raises an error)
    """

    application_mapping: dict[str, _ChannelApplication]

    def __init__(self, application_mapping: dict[str, Any]) -> None: ...
    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None: ...

@type_check_only
class _ExtendedURLPattern(URLPattern):
    callback: _ASGIApplicationProtocol | URLRouter

class URLRouter:
    """
    Routes to different applications/consumers based on the URL path.

    Works with anything that has a ``path`` key, but intended for WebSocket
    and HTTP. Uses Django's django.urls objects for resolution -
    path() or re_path().
    """

    routes: list[_ExtendedURLPattern | URLRouter]

    def __init__(self, routes: list[_ExtendedURLPattern | URLRouter]) -> None: ...
    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None: ...

class ChannelNameRouter:
    """
    Maps to different applications based on a "channel" key in the scope
    (intended for the Channels worker mode)
    """

    application_mapping: dict[str, _ChannelApplication]

    def __init__(self, application_mapping: dict[str, _ChannelApplication]) -> None: ...
    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None: ...
