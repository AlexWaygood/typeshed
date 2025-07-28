import abc
from typing import Any

from .common import RequestHandler, Response

class WebSocketResponse(Response):
    # Both raise NotImplementedError.
    def send(self, message: bytes | str) -> Any:
        """
        Send a message to the server.

        @param message: The message to send. A string (str) is sent as a text frame, bytes is sent as a binary frame.
        """

    def recv(self) -> Any: ...

class WebSocketRequestHandler(RequestHandler, abc.ABC, metaclass=abc.ABCMeta): ...
