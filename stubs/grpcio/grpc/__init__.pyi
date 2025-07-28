"""gRPC's Python API."""

import abc
import enum
import threading
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from concurrent import futures
from types import ModuleType, TracebackType
from typing import Any, Generic, NoReturn, Protocol, TypeVar, type_check_only
from typing_extensions import Self, TypeAlias

from . import aio as aio

__version__: str

_T = TypeVar("_T")

# XXX: Early attempts to tame this used literals for all the keys (gRPC is
# a bit segfaulty and doesn't adequately validate the option keys), but that
# didn't quite work out. Maybe it's something we can come back to
_OptionKeyValue: TypeAlias = tuple[str, Any]
_Options: TypeAlias = Sequence[_OptionKeyValue]

class Compression(enum.IntEnum):
    """Indicates the compression method to be used for an RPC.

    Attributes:
     NoCompression: Do not use compression algorithm.
     Deflate: Use "Deflate" compression algorithm.
     Gzip: Use "Gzip" compression algorithm.
    """

    NoCompression = 0
    Deflate = 1
    Gzip = 2

@enum.unique
class LocalConnectionType(enum.Enum):
    """Types of local connection for local credential creation.

    Attributes:
      UDS: Unix domain socket connections
      LOCAL_TCP: Local TCP connections.
    """

    UDS = 0
    LOCAL_TCP = 1

# XXX: not documented, needs more investigation.
# Some evidence:
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_metadata_test.py#L71
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_metadata_test.py#L58
# - https://github.com/grpc/grpc/blob/0e1984effd7e977ef18f1ad7fde7d10a2a153e1d/src/python/grpcio_tests/tests/unit/_invocation_defects_test.py#L66
_Metadata: TypeAlias = tuple[tuple[str, str | bytes], ...]

_TRequest = TypeVar("_TRequest")
_TResponse = TypeVar("_TResponse")
_Serializer: TypeAlias = Callable[[_T], bytes]
_Deserializer: TypeAlias = Callable[[bytes], _T]

# Future Interfaces:

class FutureTimeoutError(Exception):
    """Indicates that a method call on a Future timed out."""

class FutureCancelledError(Exception):
    """Indicates that the computation underlying a Future was cancelled."""

_TFutureValue = TypeVar("_TFutureValue")

class Future(abc.ABC, Generic[_TFutureValue]):
    """A representation of a computation in another control flow.

    Computations represented by a Future may be yet to be begun,
    may be ongoing, or may have already completed.
    """

    @abc.abstractmethod
    def add_done_callback(self, fn: Callable[[Future[_TFutureValue]], None]) -> None:
        """Adds a function to be called at completion of the computation.

        The callback will be passed this Future object describing the outcome
        of the computation.  Callbacks will be invoked after the future is
        terminated, whether successfully or not.

        If the computation has already completed, the callback will be called
        immediately.

        Exceptions raised in the callback will be logged at ERROR level, but
        will not terminate any threads of execution.

        Args:
          fn: A callable taking this Future object as its single parameter.
        """

    @abc.abstractmethod
    def cancel(self) -> bool:
        """Attempts to cancel the computation.

        This method does not block.

        Returns:
            bool:
            Returns True if the computation was canceled.

            Returns False under all other circumstances, for example:

            1. computation has begun and could not be canceled.
            2. computation has finished
            3. computation is scheduled for execution and it is impossible
                to determine its state without blocking.
        """

    @abc.abstractmethod
    def cancelled(self) -> bool:
        """Describes whether the computation was cancelled.

        This method does not block.

        Returns:
            bool:
            Returns True if the computation was cancelled before its result became
            available.

            Returns False under all other circumstances, for example:

            1. computation was not cancelled.
            2. computation's result is available.
        """

    @abc.abstractmethod
    def done(self) -> bool:
        """Describes whether the computation has taken place.

        This method does not block.

        Returns:
            bool:
            Returns True if the computation already executed or was cancelled.
            Returns False if the computation is scheduled for execution or
            currently executing.
            This is exactly opposite of the running() method's result.
        """

    @abc.abstractmethod
    def exception(self, timeout: float | None = None) -> Exception | None:
        """Return the exception raised by the computation.

        This method may return immediately or may block.

        Args:
          timeout: The length of time in seconds to wait for the computation to
            terminate or be cancelled. If None, the call will block until the
            computations's termination.

        Returns:
            The exception raised by the computation, or None if the computation
            did not raise an exception.

        Raises:
          FutureTimeoutError: If a timeout value is passed and the computation
            does not terminate within the allotted time.
          FutureCancelledError: If the computation was cancelled.
        """

    @abc.abstractmethod
    def result(self, timeout: float | None = None) -> _TFutureValue:
        """Returns the result of the computation or raises its exception.

        This method may return immediately or may block.

        Args:
          timeout: The length of time in seconds to wait for the computation to
            finish or be cancelled. If None, the call will block until the
            computations's termination.

        Returns:
          The return value of the computation.

        Raises:
          FutureTimeoutError: If a timeout value is passed and the computation
            does not terminate within the allotted time.
          FutureCancelledError: If the computation was cancelled.
          Exception: If the computation raised an exception, this call will
            raise the same exception.
        """

    @abc.abstractmethod
    def running(self) -> bool:
        """Describes whether the computation is taking place.

        This method does not block.

        Returns:
            Returns True if the computation is scheduled for execution or
            currently executing.

            Returns False if the computation already executed or was cancelled.
        """
    # FIXME: unsure of the exact return type here. Is it a traceback.StackSummary?
    @abc.abstractmethod
    def traceback(self, timeout: float | None = None):
        """Access the traceback of the exception raised by the computation.

        This method may return immediately or may block.

        Args:
          timeout: The length of time in seconds to wait for the computation
            to terminate or be cancelled. If None, the call will block until
            the computation's termination.

        Returns:
            The traceback of the exception raised by the computation, or None
            if the computation did not raise an exception.

        Raises:
          FutureTimeoutError: If a timeout value is passed and the computation
            does not terminate within the allotted time.
          FutureCancelledError: If the computation was cancelled.
        """

# Create Client:

def insecure_channel(target: str, options: _Options | None = None, compression: Compression | None = None) -> Channel:
    """Creates an insecure Channel to a server.

    The returned Channel is thread-safe.

    Args:
      target: The server address
      options: An optional list of key-value pairs (:term:`channel_arguments`
        in gRPC Core runtime) to configure the channel.
      compression: An optional value indicating the compression method to be
        used over the lifetime of the channel.

    Returns:
      A Channel.
    """

def secure_channel(
    target: str, credentials: ChannelCredentials, options: _Options | None = None, compression: Compression | None = None
) -> Channel:
    """Creates a secure Channel to a server.

    The returned Channel is thread-safe.

    Args:
      target: The server address.
      credentials: A ChannelCredentials instance.
      options: An optional list of key-value pairs (:term:`channel_arguments`
        in gRPC Core runtime) to configure the channel.
      compression: An optional value indicating the compression method to be
        used over the lifetime of the channel.

    Returns:
      A Channel.
    """

_Interceptor: TypeAlias = (
    UnaryUnaryClientInterceptor[_TRequest, _TResponse]
    | UnaryStreamClientInterceptor[_TRequest, _TResponse]
    | StreamUnaryClientInterceptor[_TRequest, _TResponse]
    | StreamStreamClientInterceptor[_TRequest, _TResponse]
)

def intercept_channel(channel: Channel, *interceptors: _Interceptor[_TRequest, _TResponse]) -> Channel:
    """Intercepts a channel through a set of interceptors.

    Args:
      channel: A Channel.
      interceptors: Zero or more objects of type
        UnaryUnaryClientInterceptor,
        UnaryStreamClientInterceptor,
        StreamUnaryClientInterceptor, or
        StreamStreamClientInterceptor.
        Interceptors are given control in the order they are listed.

    Returns:
      A Channel that intercepts each invocation via the provided interceptors.

    Raises:
      TypeError: If interceptor does not derive from any of
        UnaryUnaryClientInterceptor,
        UnaryStreamClientInterceptor,
        StreamUnaryClientInterceptor, or
        StreamStreamClientInterceptor.
    """

# Create Client Credentials:

def ssl_channel_credentials(
    root_certificates: bytes | None = None, private_key: bytes | None = None, certificate_chain: bytes | None = None
) -> ChannelCredentials:
    """Creates a ChannelCredentials for use with an SSL-enabled Channel.

    Args:
      root_certificates: The PEM-encoded root certificates as a byte string,
        or None to retrieve them from a default location chosen by gRPC
        runtime.
      private_key: The PEM-encoded private key as a byte string, or None if no
        private key should be used.
      certificate_chain: The PEM-encoded certificate chain as a byte string
        to use or None if no certificate chain should be used.

    Returns:
      A ChannelCredentials for use with an SSL-enabled Channel.
    """

def local_channel_credentials(local_connect_type: LocalConnectionType = ...) -> ChannelCredentials:
    """Creates a local ChannelCredentials used for local connections.

    This is an EXPERIMENTAL API.

    Local credentials are used by local TCP endpoints (e.g. localhost:10000)
    also UDS connections.

    The connections created by local channel credentials are not
    encrypted, but will be checked if they are local or not.
    The UDS connections are considered secure by providing peer authentication
    and data confidentiality while TCP connections are considered insecure.

    It is allowed to transmit call credentials over connections created by
    local channel credentials.

    Local channel credentials are useful for 1) eliminating insecure_channel usage;
    2) enable unit testing for call credentials without setting up secrets.

    Args:
      local_connect_type: Local connection type (either
        grpc.LocalConnectionType.UDS or grpc.LocalConnectionType.LOCAL_TCP)

    Returns:
      A ChannelCredentials for use with a local Channel
    """

def metadata_call_credentials(metadata_plugin: AuthMetadataPlugin, name: str | None = None) -> CallCredentials:
    """Construct CallCredentials from an AuthMetadataPlugin.

    Args:
      metadata_plugin: An AuthMetadataPlugin to use for authentication.
      name: An optional name for the plugin.

    Returns:
      A CallCredentials.
    """

def access_token_call_credentials(access_token: str) -> CallCredentials:
    """Construct CallCredentials from an access token.

    Args:
      access_token: A string to place directly in the http request
        authorization header, for example
        "authorization: Bearer <access_token>".

    Returns:
      A CallCredentials.
    """

def alts_channel_credentials(service_accounts: Sequence[str] | None = None) -> ChannelCredentials:
    """Creates a ChannelCredentials for use with an ALTS-enabled Channel.

    This is an EXPERIMENTAL API.
    ALTS credentials API can only be used in GCP environment as it relies on
    handshaker service being available. For more info about ALTS see
    https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security

    Args:
      service_accounts: A list of server identities accepted by the client.
        If target service accounts are provided and none of them matches the
        peer identity of the server, handshake will fail. The arg can be empty
        if the client does not have any information about trusted server
        identity.
    Returns:
      A ChannelCredentials for use with an ALTS-enabled Channel
    """

def compute_engine_channel_credentials(call_credentials: CallCredentials) -> ChannelCredentials:
    """Creates a compute engine channel credential.

    This credential can only be used in a GCP environment as it relies on
    a handshaker service. For more info about ALTS, see
    https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security

    This channel credential is expected to be used as part of a composite
    credential in conjunction with a call credentials that authenticates the
    VM's default service account. If used with any other sort of call
    credential, the connection may suddenly and unexpectedly begin failing RPCs.
    """

def xds_channel_credentials(fallback_credentials: ChannelCredentials | None = None) -> ChannelCredentials:
    """Creates a ChannelCredentials for use with xDS. This is an EXPERIMENTAL
      API.

    Args:
      fallback_credentials: Credentials to use in case it is not possible to
        establish a secure connection via xDS. If no fallback_credentials
        argument is supplied, a default SSLChannelCredentials is used.
    """

# GRPC docs say there should be at least two:
def composite_call_credentials(creds1: CallCredentials, creds2: CallCredentials, *rest: CallCredentials) -> CallCredentials:
    """Compose multiple CallCredentials to make a new CallCredentials.

    Args:
      *call_credentials: At least two CallCredentials objects.

    Returns:
      A CallCredentials object composed of the given CallCredentials objects.
    """

# Compose a ChannelCredentials and one or more CallCredentials objects.
def composite_channel_credentials(
    channel_credentials: ChannelCredentials, call_credentials: CallCredentials, *rest: CallCredentials
) -> ChannelCredentials:
    """Compose a ChannelCredentials and one or more CallCredentials objects.

    Args:
      channel_credentials: A ChannelCredentials object.
      *call_credentials: One or more CallCredentials objects.

    Returns:
      A ChannelCredentials composed of the given ChannelCredentials and
        CallCredentials objects.
    """

# Create Server:

def server(
    thread_pool: futures.ThreadPoolExecutor,
    handlers: list[GenericRpcHandler[Any, Any]] | None = None,
    interceptors: list[ServerInterceptor[Any, Any]] | None = None,
    options: _Options | None = None,
    maximum_concurrent_rpcs: int | None = None,
    compression: Compression | None = None,
    xds: bool = False,
) -> Server:
    """Creates a Server with which RPCs can be serviced.

    Args:
      thread_pool: A futures.ThreadPoolExecutor to be used by the Server
        to execute RPC handlers.
      handlers: An optional list of GenericRpcHandlers used for executing RPCs.
        More handlers may be added by calling add_generic_rpc_handlers any time
        before the server is started.
      interceptors: An optional list of ServerInterceptor objects that observe
        and optionally manipulate the incoming RPCs before handing them over to
        handlers. The interceptors are given control in the order they are
        specified. This is an EXPERIMENTAL API.
      options: An optional list of key-value pairs (:term:`channel_arguments` in gRPC runtime)
        to configure the channel.
      maximum_concurrent_rpcs: The maximum number of concurrent RPCs this server
        will service before returning RESOURCE_EXHAUSTED status, or None to
        indicate no limit.
      compression: An element of grpc.compression, e.g.
        grpc.compression.Gzip. This compression algorithm will be used for the
        lifetime of the server unless overridden.
      xds: If set to true, retrieves server configuration via xDS. This is an
        EXPERIMENTAL option.

    Returns:
      A Server object.
    """

# Create Server Credentials:

_CertificateChainPair: TypeAlias = tuple[bytes, bytes]

def ssl_server_credentials(
    private_key_certificate_chain_pairs: list[_CertificateChainPair],
    root_certificates: bytes | None = None,
    require_client_auth: bool = False,
) -> ServerCredentials:
    """Creates a ServerCredentials for use with an SSL-enabled Server.

    Args:
      private_key_certificate_chain_pairs: A list of pairs of the form
        [PEM-encoded private key, PEM-encoded certificate chain].
      root_certificates: An optional byte string of PEM-encoded client root
        certificates that the server will use to verify client authentication.
        If omitted, require_client_auth must also be False.
      require_client_auth: A boolean indicating whether or not to require
        clients to be authenticated. May only be True if root_certificates
        is not None.

    Returns:
      A ServerCredentials for use with an SSL-enabled Server. Typically, this
      object is an argument to add_secure_port() method during server setup.
    """

def local_server_credentials(local_connect_type: LocalConnectionType = ...) -> ServerCredentials:
    """Creates a local ServerCredentials used for local connections.

    This is an EXPERIMENTAL API.

    Local credentials are used by local TCP endpoints (e.g. localhost:10000)
    also UDS connections.

    The connections created by local server credentials are not
    encrypted, but will be checked if they are local or not.
    The UDS connections are considered secure by providing peer authentication
    and data confidentiality while TCP connections are considered insecure.

    It is allowed to transmit call credentials over connections created by local
    server credentials.

    Local server credentials are useful for 1) eliminating insecure_channel usage;
    2) enable unit testing for call credentials without setting up secrets.

    Args:
      local_connect_type: Local connection type (either
        grpc.LocalConnectionType.UDS or grpc.LocalConnectionType.LOCAL_TCP)

    Returns:
      A ServerCredentials for use with a local Server
    """

def ssl_server_certificate_configuration(
    private_key_certificate_chain_pairs: list[_CertificateChainPair], root_certificates: bytes | None = None
) -> ServerCertificateConfiguration:
    """Creates a ServerCertificateConfiguration for use with a Server.

    Args:
      private_key_certificate_chain_pairs: A collection of pairs of
        the form [PEM-encoded private key, PEM-encoded certificate
        chain].
      root_certificates: An optional byte string of PEM-encoded client root
        certificates that the server will use to verify client authentication.

    Returns:
      A ServerCertificateConfiguration that can be returned in the certificate
        configuration fetching callback.
    """

def dynamic_ssl_server_credentials(
    initial_certificate_configuration: ServerCertificateConfiguration,
    certificate_configuration_fetcher: Callable[[], ServerCertificateConfiguration],
    require_client_authentication: bool = False,
) -> ServerCredentials:
    """Creates a ServerCredentials for use with an SSL-enabled Server.

    Args:
      initial_certificate_configuration (ServerCertificateConfiguration): The
        certificate configuration with which the server will be initialized.
      certificate_configuration_fetcher (callable): A callable that takes no
        arguments and should return a ServerCertificateConfiguration to
        replace the server's current certificate, or None for no change
        (i.e., the server will continue its current certificate
        config). The library will call this callback on *every* new
        client connection before starting the TLS handshake with the
        client, thus allowing the user application to optionally
        return a new ServerCertificateConfiguration that the server will then
        use for the handshake.
      require_client_authentication: A boolean indicating whether or not to
        require clients to be authenticated.

    Returns:
      A ServerCredentials.
    """

def alts_server_credentials() -> ServerCredentials:
    """Creates a ServerCredentials for use with an ALTS-enabled connection.

    This is an EXPERIMENTAL API.
    ALTS credentials API can only be used in GCP environment as it relies on
    handshaker service being available. For more info about ALTS see
    https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security

    Returns:
      A ServerCredentials for use with an ALTS-enabled Server
    """

def insecure_server_credentials() -> ServerCredentials:
    """Creates a credentials object directing the server to use no credentials.
      This is an EXPERIMENTAL API.

    This object cannot be used directly in a call to `add_secure_port`.
    Instead, it should be used to construct other credentials objects, e.g.
    with xds_server_credentials.
    """

def xds_server_credentials(fallback_credentials: ServerCredentials) -> ServerCredentials:
    """Creates a ServerCredentials for use with xDS. This is an EXPERIMENTAL
      API.

    Args:
      fallback_credentials: Credentials to use in case it is not possible to
        establish a secure connection via xDS. No default value is provided.
    """

# RPC Method Handlers:

# XXX: This is probably what appears in the add_FooServicer_to_server function
# in the _pb2_grpc files that get generated, which points to the FooServicer
# handler functions that get generated, which look like this:
#
#    def FloobDoob(self, request, context):
#       return response
#
@type_check_only
class _Behaviour(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

def unary_unary_rpc_method_handler(
    behavior: _Behaviour,
    request_deserializer: _Deserializer[_TRequest] | None = None,
    response_serializer: _Serializer[_TResponse] | None = None,
) -> RpcMethodHandler[_TRequest, _TResponse]:
    """Creates an RpcMethodHandler for a unary-unary RPC method.

    Args:
      behavior: The implementation of an RPC that accepts one request
        and returns one response.
      request_deserializer: An optional :term:`deserializer` for request deserialization.
      response_serializer: An optional :term:`serializer` for response serialization.

    Returns:
      An RpcMethodHandler object that is typically used by grpc.Server.
    """

def unary_stream_rpc_method_handler(
    behavior: _Behaviour,
    request_deserializer: _Deserializer[_TRequest] | None = None,
    response_serializer: _Serializer[_TResponse] | None = None,
) -> RpcMethodHandler[_TRequest, _TResponse]:
    """Creates an RpcMethodHandler for a unary-stream RPC method.

    Args:
      behavior: The implementation of an RPC that accepts one request
        and returns an iterator of response values.
      request_deserializer: An optional :term:`deserializer` for request deserialization.
      response_serializer: An optional :term:`serializer` for response serialization.

    Returns:
      An RpcMethodHandler object that is typically used by grpc.Server.
    """

def stream_unary_rpc_method_handler(
    behavior: _Behaviour,
    request_deserializer: _Deserializer[_TRequest] | None = None,
    response_serializer: _Serializer[_TResponse] | None = None,
) -> RpcMethodHandler[_TRequest, _TResponse]:
    """Creates an RpcMethodHandler for a stream-unary RPC method.

    Args:
      behavior: The implementation of an RPC that accepts an iterator of
        request values and returns a single response value.
      request_deserializer: An optional :term:`deserializer` for request deserialization.
      response_serializer: An optional :term:`serializer` for response serialization.

    Returns:
      An RpcMethodHandler object that is typically used by grpc.Server.
    """

def stream_stream_rpc_method_handler(
    behavior: _Behaviour,
    request_deserializer: _Deserializer[_TRequest] | None = None,
    response_serializer: _Serializer[_TResponse] | None = None,
) -> RpcMethodHandler[_TRequest, _TResponse]:
    """Creates an RpcMethodHandler for a stream-stream RPC method.

    Args:
      behavior: The implementation of an RPC that accepts an iterator of
        request values and returns an iterator of response values.
      request_deserializer: An optional :term:`deserializer` for request deserialization.
      response_serializer: An optional :term:`serializer` for response serialization.

    Returns:
      An RpcMethodHandler object that is typically used by grpc.Server.
    """

def method_handlers_generic_handler(
    service: str, method_handlers: dict[str, RpcMethodHandler[Any, Any]]
) -> GenericRpcHandler[Any, Any]:
    """Creates a GenericRpcHandler from RpcMethodHandlers.

    Args:
      service: The name of the service that is implemented by the
        method_handlers.
      method_handlers: A dictionary that maps method names to corresponding
        RpcMethodHandler.

    Returns:
      A GenericRpcHandler. This is typically added to the grpc.Server object
      with add_generic_rpc_handlers() before starting the server.
    """

# Channel Ready Future:

def channel_ready_future(channel: Channel) -> Future[None]:
    """Creates a Future that tracks when a Channel is ready.

    Cancelling the Future does not affect the channel's state machine.
    It merely decouples the Future from channel state machine.

    Args:
      channel: A Channel object.

    Returns:
      A Future object that matures when the channel connectivity is
      ChannelConnectivity.READY.
    """

# Channel Connectivity:

class ChannelConnectivity(enum.Enum):
    """Mirrors grpc_connectivity_state in the gRPC Core.

    Attributes:
      IDLE: The channel is idle.
      CONNECTING: The channel is connecting.
      READY: The channel is ready to conduct RPCs.
      TRANSIENT_FAILURE: The channel has seen a failure from which it expects
        to recover.
      SHUTDOWN: The channel has seen a failure from which it cannot recover.
    """

    IDLE = (0, "idle")
    CONNECTING = (1, "connecting")
    READY = (2, "ready")
    TRANSIENT_FAILURE = (3, "transient failure")
    SHUTDOWN = (4, "shutdown")

# gRPC Status Code:

class Status(abc.ABC):
    """Describes the status of an RPC.

    This is an EXPERIMENTAL API.

    Attributes:
      code: A StatusCode object to be sent to the client.
      details: A UTF-8-encodable string to be sent to the client upon
        termination of the RPC.
      trailing_metadata: The trailing :term:`metadata` in the RPC.
    """

    code: StatusCode

    # XXX: misnamed property, does not align with status.proto, where it is called 'message':
    details: str

    trailing_metadata: _Metadata

# https://grpc.github.io/grpc/core/md_doc_statuscodes.html
class StatusCode(enum.Enum):
    """Mirrors grpc_status_code in the gRPC Core.

    Attributes:
      OK: Not an error; returned on success
      CANCELLED: The operation was cancelled (typically by the caller).
      UNKNOWN: Unknown error.
      INVALID_ARGUMENT: Client specified an invalid argument.
      DEADLINE_EXCEEDED: Deadline expired before operation could complete.
      NOT_FOUND: Some requested entity (e.g., file or directory) was not found.
      ALREADY_EXISTS: Some entity that we attempted to create (e.g., file or directory)
        already exists.
      PERMISSION_DENIED: The caller does not have permission to execute the specified
        operation.
      UNAUTHENTICATED: The request does not have valid authentication credentials for the
        operation.
      RESOURCE_EXHAUSTED: Some resource has been exhausted, perhaps a per-user quota, or
        perhaps the entire file system is out of space.
      FAILED_PRECONDITION: Operation was rejected because the system is not in a state
        required for the operation's execution.
      ABORTED: The operation was aborted, typically due to a concurrency issue
        like sequencer check failures, transaction aborts, etc.
      UNIMPLEMENTED: Operation is not implemented or not supported/enabled in this service.
      INTERNAL: Internal errors.  Means some invariants expected by underlying
        system has been broken.
      UNAVAILABLE: The service is currently unavailable.
      DATA_LOSS: Unrecoverable data loss or corruption.
    """

    OK = (0, "ok")
    CANCELLED = (1, "cancelled")
    UNKNOWN = (2, "unknown")
    INVALID_ARGUMENT = (3, "invalid argument")
    DEADLINE_EXCEEDED = (4, "deadline exceeded")
    NOT_FOUND = (5, "not found")
    ALREADY_EXISTS = (6, "already exists")
    PERMISSION_DENIED = (7, "permission denied")
    RESOURCE_EXHAUSTED = (8, "resource exhausted")
    FAILED_PRECONDITION = (9, "failed precondition")
    ABORTED = (10, "aborted")
    OUT_OF_RANGE = (11, "out of range")
    UNIMPLEMENTED = (12, "unimplemented")
    INTERNAL = (13, "internal")
    UNAVAILABLE = (14, "unavailable")
    DATA_LOSS = (15, "data loss")
    UNAUTHENTICATED = (16, "unauthenticated")

# Channel Object:

class Channel(abc.ABC):
    """Affords RPC invocation via generic methods on client-side.

    Channel objects implement the Context Manager type, although they need not
    support being entered and exited multiple times.
    """

    @abc.abstractmethod
    def close(self) -> None:
        """Closes this Channel and releases all resources held by it.

        Closing the Channel will immediately terminate all RPCs active with the
        Channel and it is not valid to invoke new RPCs with the Channel.

        This method is idempotent.
        """

    @abc.abstractmethod
    def stream_stream(
        self,
        method: str,
        request_serializer: _Serializer[_TRequest] | None = None,
        response_deserializer: _Deserializer[_TResponse] | None = None,
    ) -> StreamStreamMultiCallable[_TRequest, _TResponse]:
        """Creates a StreamStreamMultiCallable for a stream-stream method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional :term:`serializer` for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional :term:`deserializer` for deserializing the
            response message. Response goes undeserialized in case None
            is passed.
          _registered_method: Implementation Private. A bool representing whether the method
            is registered.

        Returns:
          A StreamStreamMultiCallable value for the named stream-stream method.
        """

    @abc.abstractmethod
    def stream_unary(
        self,
        method: str,
        request_serializer: _Serializer[_TRequest] | None = None,
        response_deserializer: _Deserializer[_TResponse] | None = None,
    ) -> StreamUnaryMultiCallable[_TRequest, _TResponse]:
        """Creates a StreamUnaryMultiCallable for a stream-unary method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional :term:`serializer` for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional :term:`deserializer` for deserializing the
            response message. Response goes undeserialized in case None is
            passed.
          _registered_method: Implementation Private. A bool representing whether the method
            is registered.

        Returns:
          A StreamUnaryMultiCallable value for the named stream-unary method.
        """

    @abc.abstractmethod
    def subscribe(self, callback: Callable[[ChannelConnectivity], None], try_to_connect: bool = False) -> None:
        """Subscribe to this Channel's connectivity state machine.

        A Channel may be in any of the states described by ChannelConnectivity.
        This method allows application to monitor the state transitions.
        The typical use case is to debug or gain better visibility into gRPC
        runtime's state.

        Args:
          callback: A callable to be invoked with ChannelConnectivity argument.
            ChannelConnectivity describes current state of the channel.
            The callable will be invoked immediately upon subscription
            and again for every change to ChannelConnectivity until it
            is unsubscribed or this Channel object goes out of scope.
          try_to_connect: A boolean indicating whether or not this Channel
            should attempt to connect immediately. If set to False, gRPC
            runtime decides when to connect.
        """

    @abc.abstractmethod
    def unary_stream(
        self,
        method: str,
        request_serializer: _Serializer[_TRequest] | None = None,
        response_deserializer: _Deserializer[_TResponse] | None = None,
    ) -> UnaryStreamMultiCallable[_TRequest, _TResponse]:
        """Creates a UnaryStreamMultiCallable for a unary-stream method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional :term:`serializer` for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional :term:`deserializer` for deserializing the
            response message. Response goes undeserialized in case None is
            passed.
          _registered_method: Implementation Private. A bool representing whether the method
            is registered.

        Returns:
          A UnaryStreamMultiCallable value for the name unary-stream method.
        """

    @abc.abstractmethod
    def unary_unary(
        self,
        method: str,
        request_serializer: _Serializer[_TRequest] | None = None,
        response_deserializer: _Deserializer[_TResponse] | None = None,
    ) -> UnaryUnaryMultiCallable[_TRequest, _TResponse]:
        """Creates a UnaryUnaryMultiCallable for a unary-unary method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional :term:`serializer` for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional :term:`deserializer` for deserializing the
            response message. Response goes undeserialized in case None
            is passed.
          _registered_method: Implementation Private. A bool representing whether the method
            is registered.

        Returns:
          A UnaryUnaryMultiCallable value for the named unary-unary method.
        """

    @abc.abstractmethod
    def unsubscribe(self, callback: Callable[[ChannelConnectivity], None]) -> None:
        """Unsubscribes a subscribed callback from this Channel's connectivity.

        Args:
          callback: A callable previously registered with this Channel from
          having been passed to its "subscribe" method.
        """

    def __enter__(self) -> Self:
        """Enters the runtime context related to the channel object."""

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> bool | None:
        """Exits the runtime context related to the channel object."""

# Server Object:

class Server(abc.ABC):
    """Services RPCs."""

    @abc.abstractmethod
    def add_generic_rpc_handlers(self, generic_rpc_handlers: Iterable[GenericRpcHandler[Any, Any]]) -> None:
        """Registers GenericRpcHandlers with this Server.

        This method is only safe to call before the server is started.

        Args:
          generic_rpc_handlers: An iterable of GenericRpcHandlers that will be
          used to service RPCs.
        """
    # Returns an integer port on which server will accept RPC requests.
    @abc.abstractmethod
    def add_insecure_port(self, address: str) -> int:
        """Opens an insecure port for accepting RPCs.

        This method may only be called before starting the server.

        Args:
          address: The address for which to open a port. If the port is 0,
            or not specified in the address, then gRPC runtime will choose a port.

        Returns:
          An integer port on which server will accept RPC requests.
        """
    # Returns an integer port on which server will accept RPC requests.
    @abc.abstractmethod
    def add_secure_port(self, address: str, server_credentials: ServerCredentials) -> int:
        """Opens a secure port for accepting RPCs.

        This method may only be called before starting the server.

        Args:
          address: The address for which to open a port.
            if the port is 0, or not specified in the address, then gRPC
            runtime will choose a port.
          server_credentials: A ServerCredentials object.

        Returns:
          An integer port on which server will accept RPC requests.
        """

    @abc.abstractmethod
    def start(self) -> None:
        """Starts this Server.

        This method may only be called once. (i.e. it is not idempotent).
        """
    # Grace period is in seconds.
    @abc.abstractmethod
    def stop(self, grace: float | None) -> threading.Event:
        """Stops this Server.

        This method immediately stop service of new RPCs in all cases.

        If a grace period is specified, this method waits until all active
        RPCs are finished or until the grace period is reached. RPCs that haven't
        been terminated within the grace period are aborted.
        If a grace period is not specified (by passing None for `grace`),
        all existing RPCs are aborted immediately and this method
        blocks until the last RPC handler terminates.

        This method is idempotent and may be called at any time.
        Passing a smaller grace value in a subsequent call will have
        the effect of stopping the Server sooner (passing None will
        have the effect of stopping the server immediately). Passing
        a larger grace value in a subsequent call *will not* have the
        effect of stopping the server later (i.e. the most restrictive
        grace value is used).

        Args:
          grace: A duration of time in seconds or None.

        Returns:
          A threading.Event that will be set when this Server has completely
          stopped, i.e. when running RPCs either complete or are aborted and
          all handlers have terminated.
        """
    # Block current thread until the server stops. Returns a bool
    # indicates if the operation times out. Timeout is in seconds.
    def wait_for_termination(self, timeout: float | None = None) -> bool:
        """Block current thread until the server stops.

        This is an EXPERIMENTAL API.

        The wait will not consume computational resources during blocking, and
        it will block until one of the two following conditions are met:

        1) The server is stopped or terminated;
        2) A timeout occurs if timeout is not `None`.

        The timeout argument works in the same way as `threading.Event.wait()`.
        https://docs.python.org/3/library/threading.html#threading.Event.wait

        Args:
          timeout: A floating point number specifying a timeout for the
            operation in seconds.

        Returns:
          A bool indicates if the operation times out.
        """

# Authentication & Authorization Objects:

# This class has no supported interface
class ChannelCredentials:
    """An encapsulation of the data required to create a secure Channel.

    This class has no supported interface - it exists to define the type of its
    instances and its instances exist to be passed to other functions. For
    example, ssl_channel_credentials returns an instance of this class and
    secure_channel requires an instance of this class.
    """

    def __init__(self, credentials) -> None: ...

# This class has no supported interface
class CallCredentials:
    """An encapsulation of the data required to assert an identity over a call.

    A CallCredentials has to be used with secure Channel, otherwise the
    metadata will not be transmitted to the server.

    A CallCredentials may be composed with ChannelCredentials to always assert
    identity for every call over that Channel.

    This class has no supported interface - it exists to define the type of its
    instances and its instances exist to be passed to other functions.
    """

    def __init__(self, credentials) -> None: ...

class AuthMetadataContext(abc.ABC):
    """Provides information to call credentials metadata plugins.

    Attributes:
      service_url: A string URL of the service being called into.
      method_name: A string of the fully qualified method name being called.
    """

    service_url: str
    method_name: str

class AuthMetadataPluginCallback(abc.ABC):
    """Callback object received by a metadata plugin."""

    def __call__(self, metadata: _Metadata, error: Exception | None) -> None:
        """Passes to the gRPC runtime authentication metadata for an RPC.

        Args:
          metadata: The :term:`metadata` used to construct the CallCredentials.
          error: An Exception to indicate error or None to indicate success.
        """

class AuthMetadataPlugin(abc.ABC):
    """A specification for custom authentication."""

    def __call__(self, context: AuthMetadataContext, callback: AuthMetadataPluginCallback) -> None:
        """Implements authentication by passing metadata to a callback.

        This method will be invoked asynchronously in a separate thread.

        Args:
          context: An AuthMetadataContext providing information on the RPC that
            the plugin is being called to authenticate.
          callback: An AuthMetadataPluginCallback to be invoked either
            synchronously or asynchronously.
        """

# This class has no supported interface
class ServerCredentials:
    """An encapsulation of the data required to open a secure port on a Server.

    This class has no supported interface - it exists to define the type of its
    instances and its instances exist to be passed to other functions.
    """

    def __init__(self, credentials) -> None: ...

# This class has no supported interface
class ServerCertificateConfiguration:
    """A certificate configuration for use with an SSL-enabled Server.

    Instances of this class can be returned in the certificate configuration
    fetching callback.

    This class has no supported interface -- it exists to define the
    type of its instances and its instances exist to be passed to
    other functions.
    """

    def __init__(self, certificate_configuration) -> None: ...

# gRPC Exceptions:

@type_check_only
class _Metadatum:
    key: str
    value: bytes

# FIXME: There is scant documentation about what is actually available in this type.
# The properties here are the properties observed in the wild, and may be inaccurate.
# A better source to confirm their presence needs to be found at some point.
class RpcError(Exception):
    """Raised by the gRPC library to indicate non-OK-status RPC termination."""

    def code(self) -> StatusCode: ...

    # misnamed property, does not align with status.proto, where it is called 'message':
    def details(self) -> str | None: ...

    # XXX: This has a slightly different return type to all the other metadata:
    def trailing_metadata(self) -> tuple[_Metadatum, ...]: ...

# Shared Context:

class RpcContext(abc.ABC):
    """Provides RPC-related information and action."""

    @abc.abstractmethod
    def add_callback(self, callback: Callable[[], None]) -> bool:
        """Registers a callback to be called on RPC termination.

        Args:
          callback: A no-parameter callable to be called on RPC termination.

        Returns:
          True if the callback was added and will be called later; False if
            the callback was not added and will not be called (because the RPC
            already terminated or some other reason).
        """

    @abc.abstractmethod
    def cancel(self) -> bool:
        """Cancels the RPC.

        Idempotent and has no effect if the RPC has already terminated.
        """

    @abc.abstractmethod
    def is_active(self) -> bool:
        """Describes whether the RPC is active or has terminated.

        Returns:
          bool:
          True if RPC is active, False otherwise.
        """

    @abc.abstractmethod
    def time_remaining(self) -> float:
        """Describes the length of allowed time remaining for the RPC.

        Returns:
          A nonnegative float indicating the length of allowed time in seconds
          remaining for the RPC to complete before it is considered to have
          timed out, or None if no deadline was specified for the RPC.
        """

# Client-Side Context:

class Call(RpcContext, metaclass=abc.ABCMeta):
    """Invocation-side utility object for an RPC."""

    @abc.abstractmethod
    def code(self) -> StatusCode:
        """Accesses the status code sent by the server.

        This method blocks until the value is available.

        Returns:
          The StatusCode value for the RPC.
        """
    # misnamed property, does not align with status.proto, where it is called 'message':
    @abc.abstractmethod
    def details(self) -> str:
        """Accesses the details sent by the server.

        This method blocks until the value is available.

        Returns:
          The details string of the RPC.
        """

    @abc.abstractmethod
    def initial_metadata(self) -> _Metadata:
        """Accesses the initial metadata sent by the server.

        This method blocks until the value is available.

        Returns:
          The initial :term:`metadata`.
        """

    @abc.abstractmethod
    def trailing_metadata(self) -> _Metadata:
        """Accesses the trailing metadata sent by the server.

        This method blocks until the value is available.

        Returns:
          The trailing :term:`metadata`.
        """

# Client-Side Interceptor:

class ClientCallDetails(abc.ABC):
    """Describes an RPC to be invoked.

    Attributes:
      method: The method name of the RPC.
      timeout: An optional duration of time in seconds to allow for the RPC.
      metadata: Optional :term:`metadata` to be transmitted to
        the service-side of the RPC.
      credentials: An optional CallCredentials for the RPC.
      wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
      compression: An element of grpc.compression, e.g.
        grpc.compression.Gzip.
    """

    method: str
    timeout: float | None
    metadata: _Metadata | None
    credentials: CallCredentials | None

    # "This is an EXPERIMENTAL argument. An optional flag t enable wait for ready mechanism."
    wait_for_ready: bool | None

    compression: Compression | None

# An object that is both a Call for the RPC and a Future. In the event of
# RPC completion, the return Call-Future's result value will be the
# response message of the RPC. Should the event terminate with non-OK
# status, the returned Call-Future's exception value will be an RpcError.
#
@type_check_only
class _CallFuture(Call, Future[_TResponse], metaclass=abc.ABCMeta): ...

class UnaryUnaryClientInterceptor(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords intercepting unary-unary invocations."""

    @abc.abstractmethod
    def intercept_unary_unary(
        self,
        # FIXME: decode these cryptic runes to confirm the typing mystery of
        # this callable's signature that was left for us by past civilisations:
        #
        #     continuation - A function that proceeds with the invocation by
        #     executing the next interceptor in chain or invoking the actual RPC
        #     on the underlying Channel. It is the interceptor's responsibility
        #     to call it if it decides to move the RPC forward. The interceptor
        #     can use response_future = continuation(client_call_details,
        #     request) to continue with the RPC. continuation returns an object
        #     that is both a Call for the RPC and a Future. In the event of RPC
        #     completion, the return Call-Future's result value will be the
        #     response message of the RPC. Should the event terminate with non-OK
        #     status, the returned Call-Future's exception value will be an
        #     RpcError.
        #
        continuation: Callable[[ClientCallDetails, _TRequest], _CallFuture[_TResponse]],
        client_call_details: ClientCallDetails,
        request: _TRequest,
    ) -> _CallFuture[_TResponse]:
        """Intercepts a unary-unary invocation asynchronously.

        Args:
          continuation: A function that proceeds with the invocation by
            executing the next interceptor in chain or invoking the
            actual RPC on the underlying Channel. It is the interceptor's
            responsibility to call it if it decides to move the RPC forward.
            The interceptor can use
            `response_future = continuation(client_call_details, request)`
            to continue with the RPC. `continuation` returns an object that is
            both a Call for the RPC and a Future. In the event of RPC
            completion, the return Call-Future's result value will be
            the response message of the RPC. Should the event terminate
            with non-OK status, the returned Call-Future's exception value
            will be an RpcError.
          client_call_details: A ClientCallDetails object describing the
            outgoing RPC.
          request: The request value for the RPC.

        Returns:
            An object that is both a Call for the RPC and a Future.
            In the event of RPC completion, the return Call-Future's
            result value will be the response message of the RPC.
            Should the event terminate with non-OK status, the returned
            Call-Future's exception value will be an RpcError.
        """

@type_check_only
class _CallIterator(Call, Generic[_TResponse], metaclass=abc.ABCMeta):
    def __iter__(self) -> Iterator[_TResponse]: ...
    def __next__(self) -> _TResponse: ...

class UnaryStreamClientInterceptor(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords intercepting unary-stream invocations."""

    @abc.abstractmethod
    def intercept_unary_stream(
        self,
        continuation: Callable[[ClientCallDetails, _TRequest], _CallIterator[_TResponse]],
        client_call_details: ClientCallDetails,
        request: _TRequest,
    ) -> _CallIterator[_TResponse]:
        """Intercepts a unary-stream invocation.

        Args:
          continuation: A function that proceeds with the invocation by
            executing the next interceptor in chain or invoking the
            actual RPC on the underlying Channel. It is the interceptor's
            responsibility to call it if it decides to move the RPC forward.
            The interceptor can use
            `response_iterator = continuation(client_call_details, request)`
            to continue with the RPC. `continuation` returns an object that is
            both a Call for the RPC and an iterator for response values.
            Drawing response values from the returned Call-iterator may
            raise RpcError indicating termination of the RPC with non-OK
            status.
          client_call_details: A ClientCallDetails object describing the
            outgoing RPC.
          request: The request value for the RPC.

        Returns:
            An object that is both a Call for the RPC and an iterator of
            response values. Drawing response values from the returned
            Call-iterator may raise RpcError indicating termination of
            the RPC with non-OK status. This object *should* also fulfill the
            Future interface, though it may not.
        """

class StreamUnaryClientInterceptor(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords intercepting stream-unary invocations."""

    @abc.abstractmethod
    def intercept_stream_unary(
        self,
        continuation: Callable[[ClientCallDetails, _TRequest], _CallFuture[_TResponse]],
        client_call_details: ClientCallDetails,
        request_iterator: Iterator[_TRequest],
    ) -> _CallFuture[_TResponse]:
        """Intercepts a stream-unary invocation asynchronously.

        Args:
          continuation: A function that proceeds with the invocation by
            executing the next interceptor in chain or invoking the
            actual RPC on the underlying Channel. It is the interceptor's
            responsibility to call it if it decides to move the RPC forward.
            The interceptor can use
            `response_future = continuation(client_call_details, request_iterator)`
            to continue with the RPC. `continuation` returns an object that is
            both a Call for the RPC and a Future. In the event of RPC completion,
            the return Call-Future's result value will be the response message
            of the RPC. Should the event terminate with non-OK status, the
            returned Call-Future's exception value will be an RpcError.
          client_call_details: A ClientCallDetails object describing the
            outgoing RPC.
          request_iterator: An iterator that yields request values for the RPC.

        Returns:
          An object that is both a Call for the RPC and a Future.
          In the event of RPC completion, the return Call-Future's
          result value will be the response message of the RPC.
          Should the event terminate with non-OK status, the returned
          Call-Future's exception value will be an RpcError.
        """

class StreamStreamClientInterceptor(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords intercepting stream-stream invocations."""

    @abc.abstractmethod
    def intercept_stream_stream(
        self,
        continuation: Callable[[ClientCallDetails, _TRequest], _CallIterator[_TResponse]],
        client_call_details: ClientCallDetails,
        request_iterator: Iterator[_TRequest],
    ) -> _CallIterator[_TResponse]:
        """Intercepts a stream-stream invocation.

        Args:
          continuation: A function that proceeds with the invocation by
            executing the next interceptor in chain or invoking the
            actual RPC on the underlying Channel. It is the interceptor's
            responsibility to call it if it decides to move the RPC forward.
            The interceptor can use
            `response_iterator = continuation(client_call_details, request_iterator)`
            to continue with the RPC. `continuation` returns an object that is
            both a Call for the RPC and an iterator for response values.
            Drawing response values from the returned Call-iterator may
            raise RpcError indicating termination of the RPC with non-OK
            status.
          client_call_details: A ClientCallDetails object describing the
            outgoing RPC.
          request_iterator: An iterator that yields request values for the RPC.

        Returns:
          An object that is both a Call for the RPC and an iterator of
          response values. Drawing response values from the returned
          Call-iterator may raise RpcError indicating termination of
          the RPC with non-OK status. This object *should* also fulfill the
          Future interface, though it may not.
        """

# Service-Side Context:

class ServicerContext(RpcContext, metaclass=abc.ABCMeta):
    """A context object passed to method implementations."""

    # misnamed parameter 'details', does not align with status.proto, where it is called 'message':
    @abc.abstractmethod
    def abort(self, code: StatusCode, details: str) -> NoReturn:
        """Raises an exception to terminate the RPC with a non-OK status.

        The code and details passed as arguments will supersede any existing
        ones.

        Args:
          code: A StatusCode object to be sent to the client.
            It must not be StatusCode.OK.
          details: A UTF-8-encodable string to be sent to the client upon
            termination of the RPC.

        Raises:
          Exception: An exception is always raised to signal the abortion the
            RPC to the gRPC runtime.
        """

    @abc.abstractmethod
    def abort_with_status(self, status: Status) -> NoReturn:
        """Raises an exception to terminate the RPC with a non-OK status.

        The status passed as argument will supersede any existing status code,
        status message and trailing metadata.

        This is an EXPERIMENTAL API.

        Args:
          status: A grpc.Status object. The status code in it must not be
            StatusCode.OK.

        Raises:
          Exception: An exception is always raised to signal the abortion the
            RPC to the gRPC runtime.
        """
    # FIXME: The docs say "A map of strings to an iterable of bytes for each auth property".
    # Does that mean 'bytes' (which is iterable), or 'Iterable[bytes]'?
    @abc.abstractmethod
    def auth_context(self) -> Mapping[str, bytes]:
        """Gets the auth context for the call.

        Returns:
          A map of strings to an iterable of bytes for each auth property.
        """

    def disable_next_message_compression(self) -> None:
        """Disables compression for the next response message.

        This method will override any compression configuration set during
        server creation or set on the call.
        """

    @abc.abstractmethod
    def invocation_metadata(self) -> _Metadata:
        """Accesses the metadata sent by the client.

        Returns:
          The invocation :term:`metadata`.
        """

    @abc.abstractmethod
    def peer(self) -> str:
        """Identifies the peer that invoked the RPC being serviced.

        Returns:
          A string identifying the peer that invoked the RPC being serviced.
          The string format is determined by gRPC runtime.
        """

    @abc.abstractmethod
    def peer_identities(self) -> Iterable[bytes] | None:
        """Gets one or more peer identity(s).

        Equivalent to
        servicer_context.auth_context().get(servicer_context.peer_identity_key())

        Returns:
          An iterable of the identities, or None if the call is not
          authenticated. Each identity is returned as a raw bytes type.
        """

    @abc.abstractmethod
    def peer_identity_key(self) -> str | None:
        """The auth property used to identify the peer.

        For example, "x509_common_name" or "x509_subject_alternative_name" are
        used to identify an SSL peer.

        Returns:
          The auth property (string) that indicates the
          peer identity, or None if the call is not authenticated.
        """

    @abc.abstractmethod
    def send_initial_metadata(self, initial_metadata: _Metadata) -> None:
        """Sends the initial metadata value to the client.

        This method need not be called by implementations if they have no
        metadata to add to what the gRPC runtime will transmit.

        Args:
          initial_metadata: The initial :term:`metadata`.
        """

    @abc.abstractmethod
    def set_code(self, code: StatusCode) -> None:
        """Sets the value to be used as status code upon RPC completion.

        This method need not be called by method implementations if they wish
        the gRPC runtime to determine the status code of the RPC.

        Args:
          code: A StatusCode object to be sent to the client.
        """

    def set_compression(self, compression: Compression) -> None:
        """Set the compression algorithm to be used for the entire call.

        Args:
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.
        """

    @abc.abstractmethod
    def set_trailing_metadata(self, trailing_metadata: _Metadata) -> None:
        """Sets the trailing metadata for the RPC.

        Sets the trailing metadata to be sent upon completion of the RPC.

        If this method is invoked multiple times throughout the lifetime of an
        RPC, the value supplied in the final invocation will be the value sent
        over the wire.

        This method need not be called by implementations if they have no
        metadata to add to what the gRPC runtime will transmit.

        Args:
          trailing_metadata: The trailing :term:`metadata`.
        """
    # misnamed function 'details', does not align with status.proto, where it is called 'message':
    @abc.abstractmethod
    def set_details(self, details: str) -> None:
        """Sets the value to be used as detail string upon RPC completion.

        This method need not be called by method implementations if they have
        no details to transmit.

        Args:
          details: A UTF-8-encodable string to be sent to the client upon
            termination of the RPC.
        """

    def trailing_metadata(self) -> _Metadata:
        """Access value to be used as trailing metadata upon RPC completion.

        This is an EXPERIMENTAL API.

        Returns:
          The trailing :term:`metadata` for the RPC.
        """

# Service-Side Handler:

class RpcMethodHandler(abc.ABC, Generic[_TRequest, _TResponse]):
    """An implementation of a single RPC method.

    Attributes:
      request_streaming: Whether the RPC supports exactly one request message
        or any arbitrary number of request messages.
      response_streaming: Whether the RPC supports exactly one response message
        or any arbitrary number of response messages.
      request_deserializer: A callable :term:`deserializer` that accepts a byte string and
        returns an object suitable to be passed to this object's business
        logic, or None to indicate that this object's business logic should be
        passed the raw request bytes.
      response_serializer: A callable :term:`serializer` that accepts an object produced
        by this object's business logic and returns a byte string, or None to
        indicate that the byte strings produced by this object's business logic
        should be transmitted on the wire as they are.
      unary_unary: This object's application-specific business logic as a
        callable value that takes a request value and a ServicerContext object
        and returns a response value. Only non-None if both request_streaming
        and response_streaming are False.
      unary_stream: This object's application-specific business logic as a
        callable value that takes a request value and a ServicerContext object
        and returns an iterator of response values. Only non-None if
        request_streaming is False and response_streaming is True.
      stream_unary: This object's application-specific business logic as a
        callable value that takes an iterator of request values and a
        ServicerContext object and returns a response value. Only non-None if
        request_streaming is True and response_streaming is False.
      stream_stream: This object's application-specific business logic as a
        callable value that takes an iterator of request values and a
        ServicerContext object and returns an iterator of response values.
        Only non-None if request_streaming and response_streaming are both
        True.
    """

    request_streaming: bool
    response_streaming: bool

    # XXX: not clear from docs whether this is optional or not
    request_deserializer: _Deserializer[_TRequest] | None

    # XXX: not clear from docs whether this is optional or not
    response_serializer: _Serializer[_TResponse] | None

    unary_unary: Callable[[_TRequest, ServicerContext], _TResponse] | None

    unary_stream: Callable[[_TRequest, ServicerContext], Iterator[_TResponse]] | None

    stream_unary: Callable[[Iterator[_TRequest], ServicerContext], _TResponse] | None

    stream_stream: Callable[[Iterator[_TRequest], ServicerContext], Iterator[_TResponse]] | None

class HandlerCallDetails(abc.ABC):
    """Describes an RPC that has just arrived for service.

    Attributes:
      method: The method name of the RPC.
      invocation_metadata: The :term:`metadata` sent by the client.
    """

    method: str
    invocation_metadata: _Metadata

class GenericRpcHandler(abc.ABC, Generic[_TRequest, _TResponse]):
    """An implementation of arbitrarily many RPC methods."""

    @abc.abstractmethod
    def service(self, handler_call_details: HandlerCallDetails) -> RpcMethodHandler[_TRequest, _TResponse] | None:
        """Returns the handler for servicing the RPC.

        Args:
          handler_call_details: A HandlerCallDetails describing the RPC.

        Returns:
          An RpcMethodHandler with which the RPC may be serviced if the
          implementation chooses to service this RPC, or None otherwise.
        """

class ServiceRpcHandler(GenericRpcHandler[_TRequest, _TResponse], metaclass=abc.ABCMeta):
    """An implementation of RPC methods belonging to a service.

    A service handles RPC methods with structured names of the form
    '/Service.Name/Service.Method', where 'Service.Name' is the value
    returned by service_name(), and 'Service.Method' is the method
    name.  A service can have multiple method names, but only a single
    service name.
    """

    @abc.abstractmethod
    def service_name(self) -> str:
        """Returns this service's name.

        Returns:
          The service name.
        """

# Service-Side Interceptor:

class ServerInterceptor(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords intercepting incoming RPCs on the service-side."""

    @abc.abstractmethod
    def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], RpcMethodHandler[_TRequest, _TResponse] | None],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler[_TRequest, _TResponse] | None:
        """Intercepts incoming RPCs before handing them over to a handler.

        State can be passed from an interceptor to downstream interceptors
        via contextvars. The first interceptor is called from an empty
        contextvars.Context, and the same Context is used for downstream
        interceptors and for the final handler call. Note that there are no
        guarantees that interceptors and handlers will be called from the
        same thread.

        Args:
          continuation: A function that takes a HandlerCallDetails and
            proceeds to invoke the next interceptor in the chain, if any,
            or the RPC handler lookup logic, with the call details passed
            as an argument, and returns an RpcMethodHandler instance if
            the RPC is considered serviced, or None otherwise.
          handler_call_details: A HandlerCallDetails describing the RPC.

        Returns:
          An RpcMethodHandler with which the RPC may be serviced if the
          interceptor chooses to service this RPC, or None otherwise.
        """

# Multi-Callable Interfaces:

class UnaryUnaryMultiCallable(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords invoking a unary-unary RPC from client-side."""

    @abc.abstractmethod
    def __call__(
        self,
        request: _TRequest,
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _TResponse:
        """Synchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow
            for the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
          The response value for the RPC.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """

    @abc.abstractmethod
    def future(
        self,
        request: _TRequest,
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _CallFuture[_TResponse]:
        """Asynchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
            An object that is both a Call for the RPC and a Future.
            In the event of RPC completion, the return Call-Future's result
            value will be the response message of the RPC.
            Should the event terminate with non-OK status,
            the returned Call-Future's exception value will be an RpcError.
        """

    @abc.abstractmethod
    def with_call(
        self,
        request: _TRequest,
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
        # FIXME: Return value is documented as "The response value for the RPC and a Call value for the RPC";
        # this is slightly unclear so this return type is a best-effort guess.
    ) -> tuple[_TResponse, Call]:
        """Synchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional durating of time in seconds to allow for
            the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
          The response value for the RPC and a Call value for the RPC.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """

class UnaryStreamMultiCallable(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords invoking a unary-stream RPC from client-side."""

    @abc.abstractmethod
    def __call__(
        self,
        request: _TRequest,
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _CallIterator[_TResponse]:
        """Invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC. If None, the timeout is considered infinite.
          metadata: An optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
            An object that is a Call for the RPC, an iterator of response
            values, and a Future for the RPC. Drawing response values from the
            returned Call-iterator may raise RpcError indicating termination of
            the RPC with non-OK status.
        """

class StreamUnaryMultiCallable(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords invoking a stream-unary RPC from client-side."""

    @abc.abstractmethod
    def __call__(
        self,
        request_iterator: Iterator[_TRequest],
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _TResponse:
        """Synchronously invokes the underlying RPC.

        Args:
          request_iterator: An iterator that yields request values for
            the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC. If None, the timeout is considered infinite.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
          The response value for the RPC.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also implement grpc.Call, affording methods
            such as metadata, code, and details.
        """

    @abc.abstractmethod
    def future(
        self,
        request_iterator: Iterator[_TRequest],
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _CallFuture[_TResponse]:
        """Asynchronously invokes the underlying RPC on the client.

        Args:
          request_iterator: An iterator that yields request values for the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC. If None, the timeout is considered infinite.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
            An object that is both a Call for the RPC and a Future.
            In the event of RPC completion, the return Call-Future's result value
            will be the response message of the RPC. Should the event terminate
            with non-OK status, the returned Call-Future's exception value will
            be an RpcError.
        """

    @abc.abstractmethod
    def with_call(
        self,
        request_iterator: Iterator[_TRequest],
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
        # FIXME: Return value is documented as "The response value for the RPC and a Call value for the RPC";
        # this is slightly unclear so this return type is a best-effort guess.
    ) -> tuple[_TResponse, Call]:
        """Synchronously invokes the underlying RPC on the client.

        Args:
          request_iterator: An iterator that yields request values for
            the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC. If None, the timeout is considered infinite.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
          The response value for the RPC and a Call object for the RPC.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """

class StreamStreamMultiCallable(abc.ABC, Generic[_TRequest, _TResponse]):
    """Affords invoking a stream-stream RPC on client-side."""

    @abc.abstractmethod
    def __call__(
        self,
        request_iterator: Iterator[_TRequest],
        timeout: float | None = None,
        metadata: _Metadata | None = None,
        credentials: CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: Compression | None = None,
    ) -> _CallIterator[_TResponse]:
        """Invokes the underlying RPC on the client.

        Args:
          request_iterator: An iterator that yields request values for the RPC.
          timeout: An optional duration of time in seconds to allow for
            the RPC. If not specified, the timeout is considered infinite.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: An optional flag to enable :term:`wait_for_ready` mechanism.
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip.

        Returns:
            An object that is a Call for the RPC, an iterator of response
            values, and a Future for the RPC. Drawing response values from the
            returned Call-iterator may raise RpcError indicating termination of
            the RPC with non-OK status.
        """

# Runtime Protobuf Parsing:

def protos(protobuf_path: str) -> ModuleType:
    """Returns a module generated by the indicated .proto file.

    THIS IS AN EXPERIMENTAL API.

    Use this function to retrieve classes corresponding to message
    definitions in the .proto file.

    To inspect the contents of the returned module, use the dir function.
    For example:

    ```
    protos = grpc.protos("foo.proto")
    print(dir(protos))
    ```

    The returned module object corresponds to the _pb2.py file generated
    by protoc. The path is expected to be relative to an entry on sys.path
    and all transitive dependencies of the file should also be resolvable
    from an entry on sys.path.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolvable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A module object corresponding to the message code for the indicated
      .proto file. Equivalent to a generated _pb2.py file.
    """

def services(protobuf_path: str) -> ModuleType:
    """Returns a module generated by the indicated .proto file.

    THIS IS AN EXPERIMENTAL API.

    Use this function to retrieve classes and functions corresponding to
    service definitions in the .proto file, including both stub and servicer
    definitions.

    To inspect the contents of the returned module, use the dir function.
    For example:

    ```
    services = grpc.services("foo.proto")
    print(dir(services))
    ```

    The returned module object corresponds to the _pb2_grpc.py file generated
    by protoc. The path is expected to be relative to an entry on sys.path
    and all transitive dependencies of the file should also be resolvable
    from an entry on sys.path.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolvable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A module object corresponding to the stub/service code for the indicated
      .proto file. Equivalent to a generated _pb2_grpc.py file.
    """

def protos_and_services(protobuf_path: str) -> tuple[ModuleType, ModuleType]:
    """Returns a 2-tuple of modules corresponding to protos and services.

    THIS IS AN EXPERIMENTAL API.

    The return value of this function is equivalent to a call to protos and a
    call to services.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolvable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A 2-tuple of module objects corresponding to (protos(path), services(path)).
    """
