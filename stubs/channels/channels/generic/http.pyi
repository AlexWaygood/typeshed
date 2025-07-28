from _typeshed import Unused
from collections.abc import Iterable
from typing import Any

from asgiref.typing import HTTPDisconnectEvent, HTTPRequestEvent, HTTPScope
from channels.consumer import AsyncConsumer

class AsyncHttpConsumer(AsyncConsumer):
    """
    Async HTTP consumer. Provides basic primitives for building asynchronous
    HTTP endpoints.
    """

    body: list[bytes]
    scope: HTTPScope  # type: ignore[assignment]

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...
    async def send_headers(self, *, status: int = 200, headers: Iterable[tuple[bytes, bytes]] | None = None) -> None:
        """
        Sets the HTTP response status and headers. Headers may be provided as
        a list of tuples or as a dictionary.

        Note that the ASGI spec requires that the protocol server only starts
        sending the response to the client after ``self.send_body`` has been
        called the first time.
        """

    async def send_body(self, body: bytes, *, more_body: bool = False) -> None:
        """
        Sends a response body to the client. The method expects a bytestring.

        Set ``more_body=True`` if you want to send more body content later.
        The default behavior closes the response, and further messages on
        the channel will be ignored.
        """

    async def send_response(self, status: int, body: bytes, **kwargs: Any) -> None:
        """
        Sends a response to the client. This is a thin wrapper over
        ``self.send_headers`` and ``self.send_body``, and everything said
        above applies here as well. This method may only be called once.
        """

    async def handle(self, body: bytes) -> None:
        """
        Receives the request body as a bytestring. Response may be composed
        using the ``self.send*`` methods; the return value of this method is
        thrown away.
        """

    async def disconnect(self) -> None:
        """
        Overrideable place to run disconnect handling. Do not send anything
        from here.
        """

    async def http_request(self, message: HTTPRequestEvent) -> None:
        """
        Async entrypoint - concatenates body fragments and hands off control
        to ``self.handle`` when the body has been completely received.
        """

    async def http_disconnect(self, message: HTTPDisconnectEvent) -> None:
        """
        Let the user do their cleanup and close the consumer.
        """
