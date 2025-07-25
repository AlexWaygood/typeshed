from _typeshed import SizedBuffer
from socket import socket
from typing import Literal, TypeVar, overload

from Xlib import error
from Xlib._typing import ErrorHandler
from Xlib.display import _ResourceBaseClass, _ResourceBaseClassesType
from Xlib.protocol import rq
from Xlib.support import lock
from Xlib.xobject import colormap, cursor, drawable, fontable, resource

_T = TypeVar("_T")

class bytesview:
    view: memoryview
    @overload
    def __init__(self, data: bytes | bytesview, offset: int, size: int) -> None: ...
    @overload
    def __init__(self, data: SizedBuffer, offset: int = 0, size: int | None = None) -> None: ...
    @overload
    def __getitem__(self, key: slice) -> bytes: ...
    @overload
    def __getitem__(self, key: int) -> int: ...
    def __len__(self) -> int: ...

class Display:
    extension_major_opcodes: dict[str, int]
    error_classes: dict[int, type[error.XError]]
    event_classes: dict[int, type[rq.Event] | dict[int, type[rq.Event]]]
    resource_classes: _ResourceBaseClassesType | None
    display_name: str
    default_screen: int
    socket: socket
    socket_error_lock: lock._DummyLock
    socket_error: Exception | None
    event_queue_read_lock: lock._DummyLock
    event_queue_write_lock: lock._DummyLock
    event_queue: list[rq.Event]
    request_queue_lock: lock._DummyLock
    request_serial: int
    request_queue: list[tuple[rq.Request | rq.ReplyRequest | ConnectionSetupRequest, int]]
    send_recv_lock: lock._DummyLock
    send_active: int
    recv_active: int
    event_waiting: int
    event_wait_lock: lock._DummyLock
    request_waiting: int
    request_wait_lock: lock._DummyLock
    recv_buffer_size: int
    sent_requests: list[rq.Request | rq.ReplyRequest | ConnectionSetupRequest]
    recv_packet_len: int
    data_send: bytes
    data_recv: bytes
    data_sent_bytes: int
    resource_id_lock: lock._DummyLock
    resource_ids: dict[int, None]
    last_resource_id: int
    error_handler: ErrorHandler[object] | None
    big_endian: bool
    info: ConnectionSetupRequest
    def __init__(self, display: str | None = None) -> None: ...
    def get_display_name(self) -> str: ...
    def get_default_screen(self) -> int: ...
    def fileno(self) -> int: ...
    def next_event(self) -> rq.Event: ...
    def pending_events(self) -> int: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...
    def set_error_handler(self, handler: ErrorHandler[object] | None) -> None: ...
    def allocate_resource_id(self) -> int:
        """id = d.allocate_resource_id()

        Allocate a new X resource id number ID.

        Raises ResourceIDError if there are no free resource ids.
        """

    def free_resource_id(self, rid: int) -> None:
        """d.free_resource_id(rid)

        Free resource id RID.  Attempts to free a resource id which
        isn't allocated by us are ignored.
        """

    @overload
    def get_resource_class(self, class_name: Literal["resource"], default: object = None) -> type[resource.Resource]:
        """class = d.get_resource_class(class_name, default = None)

        Return the class to be used for X resource objects of type
        CLASS_NAME, or DEFAULT if no such class is set.
        """

    @overload
    def get_resource_class(self, class_name: Literal["drawable"], default: object = None) -> type[drawable.Drawable]: ...
    @overload
    def get_resource_class(self, class_name: Literal["window"], default: object = None) -> type[drawable.Window]: ...
    @overload
    def get_resource_class(self, class_name: Literal["pixmap"], default: object = None) -> type[drawable.Pixmap]: ...
    @overload
    def get_resource_class(self, class_name: Literal["fontable"], default: object = None) -> type[fontable.Fontable]: ...
    @overload
    def get_resource_class(self, class_name: Literal["font"], default: object = None) -> type[fontable.Font]: ...
    @overload
    def get_resource_class(self, class_name: Literal["gc"], default: object = None) -> type[fontable.GC]: ...
    @overload
    def get_resource_class(self, class_name: Literal["colormap"], default: object = None) -> type[colormap.Colormap]: ...
    @overload
    def get_resource_class(self, class_name: Literal["cursor"], default: object) -> type[cursor.Cursor]: ...
    @overload
    def get_resource_class(self, class_name: str, default: _T) -> type[_ResourceBaseClass] | _T: ...
    @overload
    def get_resource_class(self, class_name: str, default: None = None) -> type[_ResourceBaseClass] | None: ...
    def set_extension_major(self, extname: str, major: int) -> None: ...
    def get_extension_major(self, extname: str) -> int: ...
    def add_extension_event(self, code: int, evt: type[rq.Event], subcode: int | None = None) -> None: ...
    def add_extension_error(self, code: int, err: type[error.XError]) -> None: ...
    def check_for_error(self) -> None: ...
    def send_request(self, request: rq.Request | rq.ReplyRequest | ConnectionSetupRequest, wait_for_response: bool) -> None: ...
    def close_internal(self, whom: object) -> None: ...
    def send_and_recv(self, flush: bool = False, event: bool = False, request: int | None = None, recv: bool = False) -> None:
        """send_and_recv(flush = None, event = None, request = None, recv = None)

        Perform I/O, or wait for some other thread to do it for us.

        send_recv_lock MUST be LOCKED when send_and_recv is called.
        It will be UNLOCKED at return.

        Exactly or one of the parameters flush, event, request and recv must
        be set to control the return condition.

        To attempt to send all requests in the queue, flush should
        be true.  Will return immediately if another thread is
        already doing send_and_recv.

        To wait for an event to be received, event should be true.

        To wait for a response to a certain request (either an error
        or a response), request should be set to that request's
        serial number.

        To just read any pending data from the server, recv should be true.

        It is not guaranteed that the return condition has been
        fulfilled when the function returns, so the caller has to loop
        until it is finished.
        """

    def parse_response(self, request: int) -> bool:
        """Internal method.

        Parse data received from server.  If REQUEST is not None
        true is returned if the request with that serial number
        was received, otherwise false is returned.

        If REQUEST is -1, we're parsing the server connection setup
        response.
        """

    def parse_error_response(self, request: int) -> bool: ...
    def default_error_handler(self, err: object) -> None: ...
    def parse_request_response(self, request: int) -> bool: ...
    def parse_event_response(self, etype: int) -> None: ...
    def get_waiting_request(self, sno: int) -> rq.ReplyRequest | ConnectionSetupRequest | None: ...
    def get_waiting_replyrequest(self) -> rq.ReplyRequest | ConnectionSetupRequest: ...
    def parse_connection_setup(self) -> bool:
        """Internal function used to parse connection setup response."""

PixmapFormat: rq.Struct
VisualType: rq.Struct
Depth: rq.Struct
Screen: rq.Struct

class ConnectionSetupRequest(rq.GetAttrData):
    def __init__(self, display: Display, *args: object, **keys: object) -> None: ...
