from _typeshed import Incomplete
from collections.abc import Callable
from typing import Any, Protocol, TypeVar

_T = TypeVar("_T")

# at runtime, socketio.namespace.BaseNamespace, but socketio isn't py.typed
class _BaseNamespace(Protocol):
    def is_asyncio_based(self) -> bool: ...
    def trigger_event(self, event: str, *args): ...

# at runtime, socketio.namespace.BaseNamespace, but socketio isn't py.typed
class _Namespace(_BaseNamespace, Protocol):
    """Base class for server-side class-based namespaces.

    A class-based namespace is a class that contains all the event handlers
    for a Socket.IO namespace. The event handlers are methods of the class
    with the prefix ``on_``, such as ``on_connect``, ``on_disconnect``,
    ``on_message``, ``on_json``, and so on.

    :param namespace: The Socket.IO namespace to be used with all the event
                      handlers defined in this class. If this argument is
                      omitted, the default namespace is used.
    """

    def emit(
        self,
        event: str,
        data=None,
        to=None,
        room: str | None = None,
        skip_sid=None,
        namespace: str | None = None,
        callback: Callable[..., Incomplete] | None = None,
        ignore_queue: bool = False,
    ):
        """Emit a custom event to one or more connected clients.

        The only difference with the :func:`socketio.Server.emit` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def send(
        self,
        data,
        to=None,
        room: str | None = None,
        skip_sid=None,
        namespace: str | None = None,
        callback: Callable[..., Incomplete] | None = None,
        ignore_queue: bool = False,
    ) -> None:
        """Send a message to one or more connected clients.

        The only difference with the :func:`socketio.Server.send` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def call(
        self, event: str, data=None, to=None, sid=None, namespace: str | None = None, timeout=None, ignore_queue: bool = False
    ):
        """Emit a custom event to a client and wait for the response.

        The only difference with the :func:`socketio.Server.call` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def enter_room(self, sid, room: str, namespace: str | None = None):
        """Enter a room.

        The only difference with the :func:`socketio.Server.enter_room` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def leave_room(self, sid, room: str, namespace: str | None = None):
        """Leave a room.

        The only difference with the :func:`socketio.Server.leave_room` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def close_room(self, room: str, namespace: str | None = None):
        """Close a room.

        The only difference with the :func:`socketio.Server.close_room` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def rooms(self, sid, namespace: str | None = None):
        """Return the rooms a client is in.

        The only difference with the :func:`socketio.Server.rooms` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def get_session(self, sid, namespace: str | None = None):
        """Return the user session for a client.

        The only difference with the :func:`socketio.Server.get_session`
        method is that when the ``namespace`` argument is not given the
        namespace associated with the class is used.
        """

    def save_session(self, sid, session, namespace: str | None = None):
        """Store the user session for a client.

        The only difference with the :func:`socketio.Server.save_session`
        method is that when the ``namespace`` argument is not given the
        namespace associated with the class is used.
        """

    def session(self, sid, namespace: str | None = None):
        """Return the user session for a client with context manager syntax.

        The only difference with the :func:`socketio.Server.session` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

    def disconnect(self, sid, namespace: str | None = None):
        """Disconnect a client.

        The only difference with the :func:`socketio.Server.disconnect` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """

class Namespace(_Namespace):
    def __init__(self, namespace: str | None = None) -> None: ...
    def trigger_event(self, event: str, *args):
        """Dispatch an event to the proper handler method.

        In the most common usage, this method is not overloaded by subclasses,
        as it performs the routing of events to methods. However, this
        method can be overridden if special dispatching rules are needed, or if
        having a single method that catches all events is desired.
        """

    def emit(  # type: ignore[override]
        self,
        event: str,
        data=None,
        room: str | None = None,
        include_self: bool = True,
        namespace: str | None = None,
        callback: Callable[..., _T] | None = None,
    ) -> _T | tuple[str, int]:
        """Emit a custom event to one or more connected clients."""

    def send(  # type: ignore[override]
        self,
        data,
        room: str | None = None,
        include_self: bool = True,
        namespace: str | None = None,
        callback: Callable[..., Any] | None = None,
    ) -> None:
        """Send a message to one or more connected clients."""

    def close_room(self, room: str, namespace: str | None = None) -> None:
        """Close a room."""
