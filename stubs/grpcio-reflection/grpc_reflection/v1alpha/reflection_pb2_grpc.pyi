"""Client and server classes corresponding to protobuf-defined services."""

from binascii import Incomplete
from typing import Final

import grpc

GRPC_GENERATED_VERSION: Final[str]
GRPC_VERSION: Final[str]

class ServerReflectionStub:
    """Missing associated documentation comment in .proto file."""

    ServerReflectionInfo: Incomplete
    def __init__(self, channel: grpc.Channel) -> None:
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """

class ServerReflectionServicer:
    """Missing associated documentation comment in .proto file."""

    def ServerReflectionInfo(self, request_iterator, context):
        """The reflection service is structured as a bidirectional stream, ensuring
        all related requests go to a single server.
        """

def add_ServerReflectionServicer_to_server(servicer, server): ...

class ServerReflection:
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ServerReflectionInfo(
        request_iterator,
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
