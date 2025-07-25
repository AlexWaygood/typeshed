from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from threading import Thread
from typing import Any, Literal, Protocol, TypedDict, TypeVar, overload
from typing_extensions import ParamSpec, TypeAlias, Unpack

from flask import Flask
from flask.testing import FlaskClient

from .namespace import Namespace as Namespace
from .test_client import SocketIOTestClient as SocketIOTestClient

_P = ParamSpec("_P")
_R_co = TypeVar("_R_co", covariant=True)
_ExceptionHandler: TypeAlias = Callable[[BaseException], _R_co]
_Handler: TypeAlias = Callable[_P, _R_co]

class _HandlerDecorator(Protocol):
    def __call__(self, handler: _Handler[_P, _R_co]) -> _Handler[_P, _R_co]: ...

class _ExceptionHandlerDecorator(Protocol):
    def __call__(self, exception_handler: _ExceptionHandler[_R_co]) -> _ExceptionHandler[_R_co]: ...

class _SocketIOServerOptions(TypedDict, total=False):
    client_manager: Incomplete
    logger: Logger | bool
    json: Incomplete
    async_handlers: bool
    always_connect: bool

class _EngineIOServerConfig(TypedDict, total=False):
    async_mode: Literal["threading", "eventlet", "gevent", "gevent_uwsgi"]
    ping_interval: float | tuple[float, float]  # seconds
    ping_timeout: float  # seconds
    max_http_buffer_size: int
    allow_upgrades: bool
    http_compression: bool
    compression_threshold: int
    cookie: str | dict[str, Any] | None
    cors_allowed_origins: str | list[str]
    cors_credentials: bool
    monitor_clients: bool
    engineio_logger: Logger | bool

class _SocketIOKwargs(_SocketIOServerOptions, _EngineIOServerConfig): ...

class SocketIO:
    """Create a Flask-SocketIO server.

    :param app: The flask application instance. If the application instance
                isn't known at the time this class is instantiated, then call
                ``socketio.init_app(app)`` once the application instance is
                available.
    :param manage_session: If set to ``True``, this extension manages the user
                           session for Socket.IO events. If set to ``False``,
                           Flask's own session management is used. When using
                           Flask's cookie based sessions it is recommended that
                           you leave this set to the default of ``True``. When
                           using server-side sessions, a ``False`` setting
                           enables sharing the user session between HTTP routes
                           and Socket.IO events.
    :param message_queue: A connection URL for a message queue service the
                          server can use for multi-process communication. A
                          message queue is not required when using a single
                          server process.
    :param channel: The channel name, when using a message queue. If a channel
                    isn't specified, a default channel will be used. If
                    multiple clusters of SocketIO processes need to use the
                    same message queue without interfering with each other,
                    then each cluster should use a different channel.
    :param path: The path where the Socket.IO server is exposed. Defaults to
                 ``'socket.io'``. Leave this as is unless you know what you are
                 doing.
    :param resource: Alias to ``path``.
    :param kwargs: Socket.IO and Engine.IO server options.

    The Socket.IO server options are detailed below:

    :param client_manager: The client manager instance that will manage the
                           client list. When this is omitted, the client list
                           is stored in an in-memory structure, so the use of
                           multiple connected servers is not possible. In most
                           cases, this argument does not need to be set
                           explicitly.
    :param logger: To enable logging set to ``True`` or pass a logger object to
                   use. To disable logging set to ``False``. The default is
                   ``False``. Note that fatal errors will be logged even when
                   ``logger`` is ``False``.
    :param json: An alternative json module to use for encoding and decoding
                 packets. Custom json modules must have ``dumps`` and ``loads``
                 functions that are compatible with the standard library
                 versions. To use the same json encoder and decoder as a Flask
                 application, use ``flask.json``.
    :param async_handlers: If set to ``True``, event handlers for a client are
                           executed in separate threads. To run handlers for a
                           client synchronously, set to ``False``. The default
                           is ``True``.
    :param always_connect: When set to ``False``, new connections are
                           provisory until the connect handler returns
                           something other than ``False``, at which point they
                           are accepted. When set to ``True``, connections are
                           immediately accepted, and then if the connect
                           handler returns ``False`` a disconnect is issued.
                           Set to ``True`` if you need to emit events from the
                           connect handler and your client is confused when it
                           receives events before the connection acceptance.
                           In any other case use the default of ``False``.

    The Engine.IO server configuration supports the following settings:

    :param async_mode: The asynchronous model to use. See the Deployment
                       section in the documentation for a description of the
                       available options. Valid async modes are ``threading``,
                       ``eventlet``, ``gevent`` and ``gevent_uwsgi``. If this
                       argument is not given, ``eventlet`` is tried first, then
                       ``gevent_uwsgi``, then ``gevent``, and finally
                       ``threading``. The first async mode that has all its
                       dependencies installed is then one that is chosen.
    :param ping_interval: The interval in seconds at which the server pings
                          the client. The default is 25 seconds. For advanced
                          control, a two element tuple can be given, where
                          the first number is the ping interval and the second
                          is a grace period added by the server.
    :param ping_timeout: The time in seconds that the client waits for the
                         server to respond before disconnecting. The default
                         is 5 seconds.
    :param max_http_buffer_size: The maximum size of a message when using the
                                 polling transport. The default is 1,000,000
                                 bytes.
    :param allow_upgrades: Whether to allow transport upgrades or not. The
                           default is ``True``.
    :param http_compression: Whether to compress packages when using the
                             polling transport. The default is ``True``.
    :param compression_threshold: Only compress messages when their byte size
                                  is greater than this value. The default is
                                  1024 bytes.
    :param cookie: If set to a string, it is the name of the HTTP cookie the
                   server sends back to the client containing the client
                   session id. If set to a dictionary, the ``'name'`` key
                   contains the cookie name and other keys define cookie
                   attributes, where the value of each attribute can be a
                   string, a callable with no arguments, or a boolean. If set
                   to ``None`` (the default), a cookie is not sent to the
                   client.
    :param cors_allowed_origins: Origin or list of origins that are allowed to
                                 connect to this server. Only the same origin
                                 is allowed by default. Set this argument to
                                 ``'*'`` to allow all origins, or to ``[]`` to
                                 disable CORS handling.
    :param cors_credentials: Whether credentials (cookies, authentication) are
                             allowed in requests to this server. The default is
                             ``True``.
    :param monitor_clients: If set to ``True``, a background task will ensure
                            inactive clients are closed. Set to ``False`` to
                            disable the monitoring task (not recommended). The
                            default is ``True``.
    :param engineio_logger: To enable Engine.IO logging set to ``True`` or pass
                            a logger object to use. To disable logging set to
                            ``False``. The default is ``False``. Note that
                            fatal errors are logged even when
                            ``engineio_logger`` is ``False``.
    """

    # This is an alias for `socketio.Server.reason` in `python-socketio`, which is not typed.
    reason: Incomplete
    # Many instance attributes are deliberately not included here,
    # as the maintainer of Flask-SocketIO considers them private, internal details:
    # https://github.com/python/typeshed/pull/10735#discussion_r1330768869
    def __init__(
        self,
        app: Flask | None = None,
        *,
        # SocketIO options
        manage_session: bool = True,
        message_queue: str | None = None,
        channel: str = "flask-socketio",
        path: str = "socket.io",
        resource: str = "socket.io",
        **kwargs: Unpack[_SocketIOKwargs],
    ) -> None: ...
    def init_app(
        self,
        app: Flask,
        *,
        # SocketIO options
        manage_session: bool = True,
        message_queue: str | None = None,
        channel: str = "flask-socketio",
        path: str = "socket.io",
        resource: str = "socket.io",
        **kwargs: Unpack[_SocketIOKwargs],
    ) -> None: ...
    def on(self, message: str, namespace: str | None = None) -> _HandlerDecorator:
        """Decorator to register a SocketIO event handler.

        This decorator must be applied to SocketIO event handlers. Example::

            @socketio.on('my event', namespace='/chat')
            def handle_my_custom_event(json):
                print('received json: ' + str(json))

        :param message: The name of the event. This is normally a user defined
                        string, but a few event names are already defined. Use
                        ``'message'`` to define a handler that takes a string
                        payload, ``'json'`` to define a handler that takes a
                        JSON blob payload, ``'connect'`` or ``'disconnect'``
                        to create handlers for connection and disconnection
                        events.
        :param namespace: The namespace on which the handler is to be
                          registered. Defaults to the global namespace.
        """

    def on_error(self, namespace: str | None = None) -> _ExceptionHandlerDecorator:
        """Decorator to define a custom error handler for SocketIO events.

        This decorator can be applied to a function that acts as an error
        handler for a namespace. This handler will be invoked when a SocketIO
        event handler raises an exception. The handler function must accept one
        argument, which is the exception raised. Example::

            @socketio.on_error(namespace='/chat')
            def chat_error_handler(e):
                print('An error has occurred: ' + str(e))

        :param namespace: The namespace for which to register the error
                          handler. Defaults to the global namespace.
        """

    def on_error_default(self, exception_handler: _ExceptionHandler[_R_co]) -> _ExceptionHandler[_R_co]:
        """Decorator to define a default error handler for SocketIO events.

        This decorator can be applied to a function that acts as a default
        error handler for any namespaces that do not have a specific handler.
        Example::

            @socketio.on_error_default
            def error_handler(e):
                print('An error has occurred: ' + str(e))
        """

    def on_event(self, message: str, handler: _Handler[[Incomplete], object], namespace: str | None = None) -> None:
        """Register a SocketIO event handler.

        ``on_event`` is the non-decorator version of ``'on'``.

        Example::

            def on_foo_event(json):
                print('received json: ' + str(json))

            socketio.on_event('my event', on_foo_event, namespace='/chat')

        :param message: The name of the event. This is normally a user defined
                        string, but a few event names are already defined. Use
                        ``'message'`` to define a handler that takes a string
                        payload, ``'json'`` to define a handler that takes a
                        JSON blob payload, ``'connect'`` or ``'disconnect'``
                        to create handlers for connection and disconnection
                        events.
        :param handler: The function that handles the event.
        :param namespace: The namespace on which the handler is to be
                          registered. Defaults to the global namespace.
        """

    @overload
    def event(self, event_handler: _Handler[_P, _R_co], /) -> _Handler[_P, _R_co]:
        """Decorator to register an event handler.

        This is a simplified version of the ``on()`` method that takes the
        event name from the decorated function.

        Example usage::

            @socketio.event
            def my_event(data):
                print('Received data: ', data)

        The above example is equivalent to::

            @socketio.on('my_event')
            def my_event(data):
                print('Received data: ', data)

        A custom namespace can be given as an argument to the decorator::

            @socketio.event(namespace='/test')
            def my_event(data):
                print('Received data: ', data)
        """

    @overload
    def event(self, namespace: str | None = None, *args, **kwargs) -> _HandlerDecorator: ...
    def on_namespace(self, namespace_handler: Namespace) -> None: ...
    def emit(
        self,
        event: str,
        *args,
        namespace: str = "/",  # / is the default (global) namespace
        to: str | None = None,
        include_self: bool = True,
        skip_sid: str | list[str] | None = None,
        callback: Callable[..., Incomplete] | None = None,
    ) -> None:
        """Emit a server generated SocketIO event.

        This function emits a SocketIO event to one or more connected clients.
        A JSON blob can be attached to the event as payload. This function can
        be used outside of a SocketIO event context, so it is appropriate to
        use when the server is the originator of an event, outside of any
        client context, such as in a regular HTTP request handler or a
        background task. Example::

            @app.route('/ping')
            def ping():
                socketio.emit('ping event', {'data': 42}, namespace='/chat')

        :param event: The name of the user event to emit.
        :param args: A dictionary with the JSON data to send as payload.
        :param namespace: The namespace under which the message is to be sent.
                          Defaults to the global namespace.
        :param to: Send the message to all the users in the given room, or to
                   the user with the given session ID. If this parameter is not
                   included, the event is sent to all connected users.
        :param include_self: ``True`` to include the sender when broadcasting
                             or addressing a room, or ``False`` to send to
                             everyone but the sender.
        :param skip_sid: The session id of a client to ignore when broadcasting
                         or addressing a room. This is typically set to the
                         originator of the message, so that everyone except
                         that client receive the message. To skip multiple sids
                         pass a list.
        :param callback: If given, this function will be called to acknowledge
                         that the client has received the message. The
                         arguments that will be passed to the function are
                         those provided by the client. Callback functions can
                         only be used when addressing an individual client.
        """

    def call(
        self,
        event: str,
        *args,
        namespace: str = "/",  # / is the default (global) namespace
        to: str | None = None,
        timeout: int = 60,  # seconds
        ignore_queue: bool = False,
    ):
        """Emit a SocketIO event and wait for the response.

        This method issues an emit with a callback and waits for the callback
        to be invoked by the client before returning. If the callback isn’t
        invoked before the timeout, then a TimeoutError exception is raised. If
        the Socket.IO connection drops during the wait, this method still waits
        until the specified timeout. Example::

            def get_status(client, data):
                status = call('status', {'data': data}, to=client)

        :param event: The name of the user event to emit.
        :param args: A dictionary with the JSON data to send as payload.
        :param namespace: The namespace under which the message is to be sent.
                          Defaults to the global namespace.
        :param to: The session ID of the recipient client.
        :param timeout: The waiting timeout. If the timeout is reached before
                        the client acknowledges the event, then a
                        ``TimeoutError`` exception is raised. The default is 60
                        seconds.
        :param ignore_queue: Only used when a message queue is configured. If
                             set to ``True``, the event is emitted to the
                             client directly, without going through the queue.
                             This is more efficient, but only works when a
                             single server process is used, or when there is a
                             single addressee. It is recommended to always
                             leave this parameter with its default value of
                             ``False``.
        """

    def send(
        self,
        data: Any,
        json: bool = False,
        namespace: str | None = None,
        to: str | None = None,
        callback: Callable[..., Incomplete] | None = None,
        include_self: bool = True,
        skip_sid: list[str] | str | None = None,
        **kwargs,
    ) -> None:
        """Send a server-generated SocketIO message.

        This function sends a simple SocketIO message to one or more connected
        clients. The message can be a string or a JSON blob. This is a simpler
        version of ``emit()``, which should be preferred. This function can be
        used outside of a SocketIO event context, so it is appropriate to use
        when the server is the originator of an event.

        :param data: The message to send, either a string or a JSON blob.
        :param json: ``True`` if ``message`` is a JSON blob, ``False``
                     otherwise.
        :param namespace: The namespace under which the message is to be sent.
                          Defaults to the global namespace.
        :param to: Send the message to all the users in the given room, or to
                   the user with the given session ID. If this parameter is not
                   included, the event is sent to all connected users.
        :param include_self: ``True`` to include the sender when broadcasting
                             or addressing a room, or ``False`` to send to
                             everyone but the sender.
        :param skip_sid: The session id of a client to ignore when broadcasting
                         or addressing a room. This is typically set to the
                         originator of the message, so that everyone except
                         that client receive the message. To skip multiple sids
                         pass a list.
        :param callback: If given, this function will be called to acknowledge
                         that the client has received the message. The
                         arguments that will be passed to the function are
                         those provided by the client. Callback functions can
                         only be used when addressing an individual client.
        """

    def close_room(self, room: str, namespace: str | None = None) -> None:
        """Close a room.

        This function removes any users that are in the given room and then
        deletes the room from the server. This function can be used outside
        of a SocketIO event context.

        :param room: The name of the room to close.
        :param namespace: The namespace under which the room exists. Defaults
                          to the global namespace.
        """

    def run(
        self,
        app,
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool = True,
        use_reloader: bool = ...,
        reloader_options: dict[str, Incomplete] = {},
        log_output: bool = ...,
        allow_unsafe_werkzeug: bool = False,
        **kwargs,
    ) -> None:
        """Run the SocketIO web server.

        :param app: The Flask application instance.
        :param host: The hostname or IP address for the server to listen on.
                     Defaults to 127.0.0.1.
        :param port: The port number for the server to listen on. Defaults to
                     5000.
        :param debug: ``True`` to start the server in debug mode, ``False`` to
                      start in normal mode.
        :param use_reloader: ``True`` to enable the Flask reloader, ``False``
                             to disable it.
        :param reloader_options: A dictionary with options that are passed to
                                 the Flask reloader, such as ``extra_files``,
                                 ``reloader_type``, etc.
        :param extra_files: A list of additional files that the Flask
                            reloader should watch. Defaults to ``None``.
                            Deprecated, use ``reloader_options`` instead.
        :param log_output: If ``True``, the server logs all incoming
                           connections. If ``False`` logging is disabled.
                           Defaults to ``True`` in debug mode, ``False``
                           in normal mode. Unused when the threading async
                           mode is used.
        :param allow_unsafe_werkzeug: Set to ``True`` to allow the use of the
                                      Werkzeug web server in a production
                                      setting. Default is ``False``. Set to
                                      ``True`` at your own risk.
        :param kwargs: Additional web server options. The web server options
                       are specific to the server used in each of the supported
                       async modes. Note that options provided here will
                       not be seen when using an external web server such
                       as gunicorn, since this method is not called in that
                       case.
        """

    def stop(self) -> None:
        """Stop a running SocketIO web server.

        This method must be called from a HTTP or SocketIO handler function.
        """

    def start_background_task(self, target: Callable[_P, None], *args: _P.args, **kwargs: _P.kwargs) -> Thread:
        """Start a background task using the appropriate async model.

        This is a utility function that applications can use to start a
        background task using the method that is compatible with the
        selected async mode.

        :param target: the target function to execute.
        :param args: arguments to pass to the function.
        :param kwargs: keyword arguments to pass to the function.

        This function returns an object that represents the background task,
        on which the ``join()`` method can be invoked to wait for the task to
        complete.
        """

    def sleep(self, seconds: int = 0):
        """Sleep for the requested amount of time using the appropriate async
        model.

        This is a utility function that applications can use to put a task to
        sleep without having to worry about using the correct call for the
        selected async mode.
        """

    def test_client(
        self,
        app: Flask,
        namespace: str | None = None,
        query_string: str | None = None,
        headers: dict[str, Incomplete] | None = None,
        auth: dict[str, Incomplete] | None = None,
        flask_test_client: FlaskClient | None = None,
    ) -> SocketIOTestClient:
        """The Socket.IO test client is useful for testing a Flask-SocketIO
        server. It works in a similar way to the Flask Test Client, but
        adapted to the Socket.IO server.

        :param app: The Flask application instance.
        :param namespace: The namespace for the client. If not provided, the
                          client connects to the server on the global
                          namespace.
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

def emit(
    event,
    *args,
    namespace: str = "/",  # / is the default (global) namespace
    to: str | None = None,
    include_self: bool = True,
    skip_sid: str | list[str] | None = None,
    callback: Callable[..., Incomplete] | None = None,
    broadcast: bool = False,
) -> None:
    """Emit a SocketIO event.

    This function emits a SocketIO event to one or more connected clients. A
    JSON blob can be attached to the event as payload. This is a function that
    can only be called from a SocketIO event handler, as in obtains some
    information from the current client context. Example::

        @socketio.on('my event')
        def handle_my_custom_event(json):
            emit('my response', {'data': 42})

    :param event: The name of the user event to emit.
    :param args: A dictionary with the JSON data to send as payload.
    :param namespace: The namespace under which the message is to be sent.
                      Defaults to the namespace used by the originating event.
                      A ``'/'`` can be used to explicitly specify the global
                      namespace.
    :param callback: Callback function to invoke with the client's
                     acknowledgement.
    :param broadcast: ``True`` to send the message to all clients, or ``False``
                      to only reply to the sender of the originating event.
    :param to: Send the message to all the users in the given room, or to the
               user with the given session ID. If this argument is not set and
               ``broadcast`` is ``False``, then the message is sent only to the
               originating user.
    :param include_self: ``True`` to include the sender when broadcasting or
                         addressing a room, or ``False`` to send to everyone
                         but the sender.
    :param skip_sid: The session id of a client to ignore when broadcasting
                     or addressing a room. This is typically set to the
                     originator of the message, so that everyone except
                     that client receive the message. To skip multiple sids
                     pass a list.
    :param ignore_queue: Only used when a message queue is configured. If
                         set to ``True``, the event is emitted to the
                         clients directly, without going through the queue.
                         This is more efficient, but only works when a
                         single server process is used, or when there is a
                         single addressee. It is recommended to always leave
                         this parameter with its default value of ``False``.
    """

def send(message: str, **kwargs) -> None:
    """Send a SocketIO message.

    This function sends a simple SocketIO message to one or more connected
    clients. The message can be a string or a JSON blob. This is a simpler
    version of ``emit()``, which should be preferred. This is a function that
    can only be called from a SocketIO event handler.

    :param message: The message to send, either a string or a JSON blob.
    :param json: ``True`` if ``message`` is a JSON blob, ``False``
                     otherwise.
    :param namespace: The namespace under which the message is to be sent.
                      Defaults to the namespace used by the originating event.
                      An empty string can be used to use the global namespace.
    :param callback: Callback function to invoke with the client's
                     acknowledgement.
    :param broadcast: ``True`` to send the message to all connected clients, or
                      ``False`` to only reply to the sender of the originating
                      event.
    :param to: Send the message to all the users in the given room, or to the
               user with the given session ID. If this argument is not set and
               ``broadcast`` is ``False``, then the message is sent only to the
               originating user.
    :param include_self: ``True`` to include the sender when broadcasting or
                         addressing a room, or ``False`` to send to everyone
                         but the sender.
    :param skip_sid: The session id of a client to ignore when broadcasting
                     or addressing a room. This is typically set to the
                     originator of the message, so that everyone except
                     that client receive the message. To skip multiple sids
                     pass a list.
    :param ignore_queue: Only used when a message queue is configured. If
                         set to ``True``, the event is emitted to the
                         clients directly, without going through the queue.
                         This is more efficient, but only works when a
                         single server process is used, or when there is a
                         single addressee. It is recommended to always leave
                         this parameter with its default value of ``False``.
    """

def join_room(room, sid: str | None = None, namespace: str | None = None) -> None:
    """Join a room.

    This function puts the user in a room, under the current namespace. The
    user and the namespace are obtained from the event context. This is a
    function that can only be called from a SocketIO event handler. Example::

        @socketio.on('join')
        def on_join(data):
            username = session['username']
            room = data['room']
            join_room(room)
            send(username + ' has entered the room.', to=room)

    :param room: The name of the room to join.
    :param sid: The session id of the client. If not provided, the client is
                obtained from the request context.
    :param namespace: The namespace for the room. If not provided, the
                      namespace is obtained from the request context.
    """

def leave_room(room, sid: str | None = None, namespace: str | None = None) -> None:
    """Leave a room.

    This function removes the user from a room, under the current namespace.
    The user and the namespace are obtained from the event context. Example::

        @socketio.on('leave')
        def on_leave(data):
            username = session['username']
            room = data['room']
            leave_room(room)
            send(username + ' has left the room.', to=room)

    :param room: The name of the room to leave.
    :param sid: The session id of the client. If not provided, the client is
                obtained from the request context.
    :param namespace: The namespace for the room. If not provided, the
                      namespace is obtained from the request context.
    """

def close_room(room, namespace: str | None = None) -> None:
    """Close a room.

    This function removes any users that are in the given room and then deletes
    the room from the server.

    :param room: The name of the room to close.
    :param namespace: The namespace for the room. If not provided, the
                      namespace is obtained from the request context.
    """

def rooms(sid: str | None = None, namespace: str | None = None) -> list[str]:
    """Return a list of the rooms the client is in.

    This function returns all the rooms the client has entered, including its
    own room, assigned by the Socket.IO server.

    :param sid: The session id of the client. If not provided, the client is
                obtained from the request context.
    :param namespace: The namespace for the room. If not provided, the
                      namespace is obtained from the request context.
    """

def disconnect(sid: str | None = None, namespace: str | None = None, silent: bool = False) -> None:
    """Disconnect the client.

    This function terminates the connection with the client. As a result of
    this call the client will receive a disconnect event. Example::

        @socketio.on('message')
        def receive_message(msg):
            if is_banned(session['username']):
                disconnect()
            else:
                # ...

    :param sid: The session id of the client. If not provided, the client is
                obtained from the request context.
    :param namespace: The namespace for the room. If not provided, the
                      namespace is obtained from the request context.
    :param silent: this option is deprecated.
    """
