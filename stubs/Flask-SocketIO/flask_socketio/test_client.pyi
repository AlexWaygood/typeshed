from _typeshed import Incomplete
from typing import Any, TypedDict

from flask import Flask
from flask.testing import FlaskClient

class _Packet(TypedDict):
    name: str
    args: Any
    namespace: str

class SocketIOTestClient:
    """
    This class is useful for testing a Flask-SocketIO server. It works in a
    similar way to the Flask Test Client, but adapted to the Socket.IO server.

    :param app: The Flask application instance.
    :param socketio: The application's ``SocketIO`` instance.
    :param namespace: The namespace for the client. If not provided, the client
                      connects to the server on the global namespace.
    :param query_string: A string with custom query string arguments.
    :param headers: A dictionary with custom HTTP headers.
    :param auth: Optional authentication data, given as a dictionary.
    :param flask_test_client: The instance of the Flask test client
                              currently in use. Passing the Flask test
                              client is optional, but is necessary if you
                              want the Flask user session and any other
                              cookies set in HTTP routes accessible from
                              Socket.IO events.
    """

    def __init__(
        self,
        app: Flask,
        socketio,
        namespace: str | None = None,
        query_string: str | None = None,
        headers: dict[str, Incomplete] | None = None,
        auth: dict[str, Incomplete] | None = None,
        flask_test_client: FlaskClient | None = None,
    ) -> None: ...
    def is_connected(self, namespace: str | None = None) -> bool:
        """Check if a namespace is connected.

        :param namespace: The namespace to check. The global namespace is
                         assumed if this argument is not provided.
        """

    def connect(
        self,
        namespace: str | None = None,
        query_string: str | None = None,
        headers: dict[str, Incomplete] | None = None,
        auth: dict[str, Incomplete] | None = None,
    ) -> None:
        """Connect the client.

        :param namespace: The namespace for the client. If not provided, the
                          client connects to the server on the global
                          namespace.
        :param query_string: A string with custom query string arguments.
        :param headers: A dictionary with custom HTTP headers.
        :param auth: Optional authentication data, given as a dictionary.

        Note that it is usually not necessary to explicitly call this method,
        since a connection is automatically established when an instance of
        this class is created. An example where it this method would be useful
        is when the application accepts multiple namespace connections.
        """

    def disconnect(self, namespace: str | None = None) -> None:
        """Disconnect the client.

        :param namespace: The namespace to disconnect. The global namespace is
                         assumed if this argument is not provided.
        """

    def emit(self, event: str, *args, callback: bool = False, namespace: str | None = None) -> Incomplete | None:
        """Emit an event to the server.

        :param event: The event name.
        :param *args: The event arguments.
        :param callback: ``True`` if the client requests a callback, ``False``
                         if not. Note that client-side callbacks are not
                         implemented, a callback request will just tell the
                         server to provide the arguments to invoke the
                         callback, but no callback is invoked. Instead, the
                         arguments that the server provided for the callback
                         are returned by this function.
        :param namespace: The namespace of the event. The global namespace is
                          assumed if this argument is not provided.
        """

    def send(
        self,
        data: str | dict[str, Incomplete] | list[Incomplete],
        json: bool = False,
        callback: bool = False,
        namespace: str | None = None,
    ):
        """Send a text or JSON message to the server.

        :param data: A string, dictionary or list to send to the server.
        :param json: ``True`` to send a JSON message, ``False`` to send a text
                     message.
        :param callback: ``True`` if the client requests a callback, ``False``
                         if not. Note that client-side callbacks are not
                         implemented, a callback request will just tell the
                         server to provide the arguments to invoke the
                         callback, but no callback is invoked. Instead, the
                         arguments that the server provided for the callback
                         are returned by this function.
        :param namespace: The namespace of the event. The global namespace is
                          assumed if this argument is not provided.
        """

    def get_received(self, namespace: str | None = None) -> list[_Packet]:
        """Return the list of messages received from the server.

        Since this is not a real client, any time the server emits an event,
        the event is simply stored. The test code can invoke this method to
        obtain the list of events that were received since the last call.

        :param namespace: The namespace to get events from. The global
                          namespace is assumed if this argument is not
                          provided.
        """
