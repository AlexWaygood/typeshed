"""X-Resource extension allows a client to query the X server about its usage
of various resources.

For detailed description see any of the following documents.
Protocol specification:
    https://www.x.org/releases/current/doc/resourceproto/resproto.txt
XCB Protocol specification:
    https://cgit.freedesktop.org/xcb/proto/tree/src/res.xml
"""

from _typeshed import Unused
from collections.abc import Sequence
from typing import Final

from Xlib.display import Display
from Xlib.protocol import rq
from Xlib.xobject import resource

RES_MAJOR_VERSION: Final = 1
RES_MINOR_VERSION: Final = 2
extname: Final = "X-Resource"
ResQueryVersion: Final = 0
ResQueryClients: Final = 1
ResQueryClientResources: Final = 2
ResQueryClientPixmapBytes: Final = 3
ResQueryClientIds: Final = 4
ResQueryResourceBytes: Final = 5

class QueryVersion(rq.ReplyRequest): ...

def query_version(self: Display | resource.Resource, client_major: int = 1, client_minor: int = 2) -> QueryVersion:
    """Query the protocol version supported by the X server.

    The client sends the highest supported version to the server and the
    server sends the highest version it supports, but no higher than the
    requested version.
    """

Client: rq.Struct

class QueryClients(rq.ReplyRequest): ...

def query_clients(self: Display | resource.Resource) -> QueryClients:
    """Request the list of all currently connected clients."""

Type: rq.Struct

class QueryClientResources(rq.ReplyRequest): ...

def query_client_resources(self: Display | resource.Resource, client: int) -> QueryClientResources:
    """Request the number of resources owned by a client.

    The server will return the counts of each type of resource.
    """

class QueryClientPixmapBytes(rq.ReplyRequest): ...

def query_client_pixmap_bytes(self: Display | resource.Resource, client: int) -> QueryClientPixmapBytes:
    """Query the pixmap usage of some client.

    The returned number is a sum of memory usage of each pixmap that can be
    attributed to the given client.
    """

class SizeOf(rq.LengthOf):
    """A SizeOf stores the size in bytes of some other Field whose size
    may vary, e.g. List
    """

    item_size: int
    def __init__(self, name: str | list[str] | tuple[str, ...], size: int, item_size: int) -> None: ...
    def parse_value(self, length: int, display: Unused) -> int: ...  # type: ignore[override]

ClientXIDMask: Final = 0x1
LocalClientPIDMask: Final = 0x2
ClientIdSpec: rq.Struct
ClientIdValue: rq.Struct

class QueryClientIds(rq.ReplyRequest): ...

def query_client_ids(self: Display | resource.Resource, specs: Sequence[tuple[int, int]]) -> QueryClientIds:
    """Request to identify a given set of clients with some identification method.

    The request sends a list of specifiers that select clients and
    identification methods to server. The server then tries to identify the
    chosen clients using the identification methods specified for each client.
    The server returns IDs for those clients that were successfully identified.
    """

ResourceIdSpec: rq.Struct
ResourceSizeSpec: rq.Struct
ResourceSizeValue: rq.Struct

class QueryResourceBytes(rq.ReplyRequest): ...

def query_resource_bytes(self: Display | resource.Resource, client: int, specs: Sequence[tuple[int, int]]) -> QueryResourceBytes:
    """Query the sizes of resources from X server.

    The request sends a list of specifiers that selects resources for size
    calculation. The server tries to calculate the sizes of chosen resources
    and returns an estimate for a resource only if the size could be determined
    """

def init(disp: Display, info: Unused) -> None: ...
