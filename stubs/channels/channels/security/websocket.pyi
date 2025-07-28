from collections.abc import Iterable
from re import Pattern
from typing import Any
from urllib.parse import ParseResult

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable
from channels.consumer import _ChannelScope
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.utils import _ChannelApplication

class OriginValidator:
    """
    Validates that the incoming connection has an Origin header that
    is in an allowed list.
    """

    application: _ChannelApplication
    allowed_origins: Iterable[str | Pattern[str]]

    def __init__(self, application: _ChannelApplication, allowed_origins: Iterable[str | Pattern[str]]) -> None: ...
    async def __call__(self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> Any: ...
    def valid_origin(self, parsed_origin: ParseResult | None) -> bool:
        """
        Checks parsed origin is None.

        Pass control to the validate_origin function.

        Returns ``True`` if validation function was successful, ``False`` otherwise.
        """

    def validate_origin(self, parsed_origin: ParseResult | None) -> bool:
        """
        Validate the given origin for this site.

        Check than the origin looks valid and matches the origin pattern in
        specified list ``allowed_origins``. Any pattern begins with a scheme.
        After the scheme there must be a domain. Any domain beginning with a
        period corresponds to the domain and all its subdomains (for example,
        ``http://.example.com``). After the domain there must be a port,
        but it can be omitted. ``*`` matches anything and anything
        else must match exactly.

        Note. This function assumes that the given origin has a schema, domain
        and port, but port is optional.

        Returns ``True`` for a valid host, ``False`` otherwise.
        """

    def match_allowed_origin(self, parsed_origin: ParseResult | None, pattern: str | Pattern[str]) -> bool:
        """
        Returns ``True`` if the origin is either an exact match or a match
        to the wildcard pattern. Compares scheme, domain, port of origin and pattern.

        Any pattern can be begins with a scheme. After the scheme must be a domain,
        or just domain without scheme.
        Any domain beginning with a period corresponds to the domain and all
        its subdomains (for example, ``.example.com`` ``example.com``
        and any subdomain). Also with scheme (for example, ``http://.example.com``
        ``http://exapmple.com``). After the domain there must be a port,
        but it can be omitted.

        Note. This function assumes that the given origin is either None, a
        schema-domain-port string, or just a domain string
        """

    def get_origin_port(self, origin: ParseResult | None) -> int | None:
        """
        Returns the origin.port or port for this schema by default.
        Otherwise, it returns None.
        """

def AllowedHostsOriginValidator(application: _ChannelApplication) -> OriginValidator:
    """
    Factory function which returns an OriginValidator configured to use
    settings.ALLOWED_HOSTS.
    """

class WebsocketDenier(AsyncWebsocketConsumer):
    """
    Simple application which denies all requests to it.
    """

    async def connect(self) -> None: ...
