from _typeshed import Unused
from typing import Any

from asgiref.typing import WebSocketConnectEvent, WebSocketDisconnectEvent, WebSocketReceiveEvent
from channels.consumer import AsyncConsumer, SyncConsumer

class WebsocketConsumer(SyncConsumer):
    """
    Base WebSocket consumer. Provides a general encapsulation for the
    WebSocket handling model that other applications can build on.
    """

    groups: list[str]

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...
    def websocket_connect(self, message: WebSocketConnectEvent) -> None:
        """
        Called when a WebSocket connection is opened.
        """

    def connect(self) -> None: ...
    def accept(self, subprotocol: str | None = None, headers: list[tuple[str, str]] | None = None) -> None:
        """
        Accepts an incoming socket
        """

    def websocket_receive(self, message: WebSocketReceiveEvent) -> None:
        """
        Called when a WebSocket frame is received. Decodes it and passes it
        to receive().
        """

    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        """
        Called with a decoded WebSocket frame.
        """

    def send(  # type: ignore[override]
        self, text_data: str | None = None, bytes_data: bytes | None = None, close: bool = False
    ) -> None:
        """
        Sends a reply back down the WebSocket
        """

    def close(self, code: int | bool | None = None, reason: str | None = None) -> None:
        """
        Closes the WebSocket from the server end
        """

    def websocket_disconnect(self, message: WebSocketDisconnectEvent) -> None:
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """

    def disconnect(self, code: int) -> None:
        """
        Called when a WebSocket connection is closed.
        """

class JsonWebsocketConsumer(WebsocketConsumer):
    """
    Variant of WebsocketConsumer that automatically JSON-encodes and decodes
    messages as they come in and go out. Expects everything to be text; will
    error on binary data.
    """

    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None, **kwargs: Any) -> None: ...
    # content is typed as Any to match json.loads() return type - JSON can represent
    # various Python types (dict, list, str, int, float, bool, None)
    def receive_json(self, content: Any, **kwargs: Any) -> None:
        """
        Called with decoded JSON content.
        """
    # content is typed as Any to match json.dumps() input type - accepts any JSON-serializable object
    def send_json(self, content: Any, close: bool = False) -> None:
        """
        Encode the given content as JSON and send it to the client.
        """

    @classmethod
    def decode_json(cls, text_data: str) -> Any: ...  # Returns Any like json.loads()
    @classmethod
    def encode_json(cls, content: Any) -> str: ...  # Accepts Any like json.dumps()

class AsyncWebsocketConsumer(AsyncConsumer):
    """
    Base WebSocket consumer, async version. Provides a general encapsulation
    for the WebSocket handling model that other applications can build on.
    """

    groups: list[str]

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...
    async def websocket_connect(self, message: WebSocketConnectEvent) -> None:
        """
        Called when a WebSocket connection is opened.
        """

    async def connect(self) -> None: ...
    async def accept(self, subprotocol: str | None = None, headers: list[tuple[str, str]] | None = None) -> None:
        """
        Accepts an incoming socket
        """

    async def websocket_receive(self, message: WebSocketReceiveEvent) -> None:
        """
        Called when a WebSocket frame is received. Decodes it and passes it
        to receive().
        """

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        """
        Called with a decoded WebSocket frame.
        """

    async def send(  # type: ignore[override]
        self, text_data: str | None = None, bytes_data: bytes | None = None, close: bool = False
    ) -> None:
        """
        Sends a reply back down the WebSocket
        """

    async def close(self, code: int | bool | None = None, reason: str | None = None) -> None:
        """
        Closes the WebSocket from the server end
        """

    async def websocket_disconnect(self, message: WebSocketDisconnectEvent) -> None:
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """

    async def disconnect(self, code: int) -> None:
        """
        Called when a WebSocket connection is closed.
        """

class AsyncJsonWebsocketConsumer(AsyncWebsocketConsumer):
    """
    Variant of AsyncWebsocketConsumer that automatically JSON-encodes and decodes
    messages as they come in and go out. Expects everything to be text; will
    error on binary data.
    """

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None, **kwargs: Any) -> None: ...
    # content is typed as Any to match json.loads() return type - JSON can represent
    # various Python types (dict, list, str, int, float, bool, None)
    async def receive_json(self, content: Any, **kwargs: Any) -> None:
        """
        Called with decoded JSON content.
        """
    # content is typed as Any to match json.dumps() input type - accepts any JSON-serializable object
    async def send_json(self, content: Any, close: bool = False) -> None:
        """
        Encode the given content as JSON and send it to the client.
        """

    @classmethod
    async def decode_json(cls, text_data: str) -> Any: ...  # Returns Any like json.loads()
    @classmethod
    async def encode_json(cls, content: Any) -> str: ...  # Accepts Any like json.dumps()
