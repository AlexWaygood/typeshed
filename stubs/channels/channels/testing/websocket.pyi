from collections.abc import Iterable
from typing import Any, Literal, TypedDict, overload, type_check_only
from typing_extensions import NotRequired, TypeAlias

from asgiref.typing import ASGIVersions
from channels.testing.application import ApplicationCommunicator
from channels.utils import _ChannelApplication

@type_check_only
class _WebsocketTestScope(TypedDict, total=False):
    spec_version: int
    type: Literal["websocket"]
    asgi: ASGIVersions
    http_version: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[tuple[bytes, bytes]] | None
    client: tuple[str, int] | None
    server: tuple[str, int | None] | None
    subprotocols: Iterable[str] | None
    state: NotRequired[dict[str, Any]]
    extensions: dict[str, dict[object, object]] | None

_Connected: TypeAlias = bool
_CloseCodeOrAcceptSubProtocol: TypeAlias = int | str | None
_WebsocketConnectResponse: TypeAlias = tuple[_Connected, _CloseCodeOrAcceptSubProtocol]

class WebsocketCommunicator(ApplicationCommunicator):
    """
    ApplicationCommunicator subclass that has WebSocket shortcut methods.

    It will construct the scope for you, so you need to pass the application
    (uninstantiated) along with the initial connection parameters.
    """

    scope: _WebsocketTestScope
    response_headers: list[tuple[bytes, bytes]] | None

    def __init__(
        self,
        application: _ChannelApplication,
        path: str,
        headers: Iterable[tuple[bytes, bytes]] | None = None,
        subprotocols: Iterable[str] | None = None,
        spec_version: int | None = None,
    ) -> None: ...
    async def connect(self, timeout: float = 1) -> _WebsocketConnectResponse:
        """
        Trigger the connection code.

        On an accepted connection, returns (True, <chosen-subprotocol>)
        On a rejected connection, returns (False, <close-code>)
        """

    async def send_to(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        """
        Sends a WebSocket frame to the application.
        """

    async def receive_from(self, timeout: float = 1) -> str | bytes:
        """
        Receives a data frame from the view. Will fail if the connection
        closes instead. Returns either a bytestring or a unicode string
        depending on what sort of frame you got.
        """
    # These overloads reflect common usage, where users typically send and receive `dict[str, Any]`.
    # The base case allows `Any` to support broader `json.dumps` / `json.loads` compatibility.
    @overload
    async def send_json_to(self, data: dict[str, Any]) -> None:
        """
        Sends JSON data as a text frame
        """

    @overload
    async def send_json_to(self, data: Any) -> None: ...
    async def receive_json_from(self, timeout: float = 1) -> Any:
        """
        Receives a JSON text frame payload and decodes it
        """

    async def disconnect(self, code: int = 1000, timeout: float = 1) -> None:
        """
        Closes the socket
        """
