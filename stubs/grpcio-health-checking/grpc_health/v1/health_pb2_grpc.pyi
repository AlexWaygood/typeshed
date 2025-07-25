"""Client and server classes corresponding to protobuf-defined services."""

from typing import Final

GRPC_GENERATED_VERSION: Final[str]
GRPC_VERSION: Final[str]

class HealthStub:
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel) -> None:
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """

class HealthServicer:
    """Missing associated documentation comment in .proto file."""

    def Check(self, request, context):
        """If the requested service is unknown, the call will fail with status
        NOT_FOUND.
        """

    def Watch(self, request, context):
        """Performs a watch for the serving status of the requested service.
        The server will immediately send back a message indicating the current
        serving status.  It will then subsequently send a new message whenever
        the service's serving status changes.

        If the requested service is unknown when the call is received, the
        server will send a message setting the serving status to
        SERVICE_UNKNOWN but will *not* terminate the call.  If at some
        future point, the serving status of the service becomes known, the
        server will send a new message with the service's serving status.

        If the call terminates with status UNIMPLEMENTED, then clients
        should assume this method is not supported and should not retry the
        call.  If the call terminates with any other status (including OK),
        clients should retry the call with appropriate exponential backoff.
        """

def add_HealthServicer_to_server(servicer, server) -> None: ...

class Health:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Check(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ): ...
    @staticmethod
    def Watch(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ): ...
