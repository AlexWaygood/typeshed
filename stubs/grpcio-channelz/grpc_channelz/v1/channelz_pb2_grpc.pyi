"""Client and server classes corresponding to protobuf-defined services."""

from _typeshed import Incomplete
from typing import Final

import grpc

GRPC_GENERATED_VERSION: Final[str]
GRPC_VERSION: Final[str]

class ChannelzStub:
    """Channelz is a service exposed by gRPC servers that provides detailed debug
    information.
    """

    GetTopChannels: Incomplete
    GetServers: Incomplete
    GetServer: Incomplete
    GetServerSockets: Incomplete
    GetChannel: Incomplete
    GetSubchannel: Incomplete
    GetSocket: Incomplete
    def __init__(self, channel: grpc.Channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """

class ChannelzServicer:
    """Channelz is a service exposed by gRPC servers that provides detailed debug
    information.
    """

    def GetTopChannels(self, request, context):
        """Gets all root channels (i.e. channels the application has directly
        created). This does not include subchannels nor non-top level channels.
        """

    def GetServers(self, request, context):
        """Gets all servers that exist in the process."""

    def GetServer(self, request, context):
        """Returns a single Server, or else a NOT_FOUND code."""

    def GetServerSockets(self, request, context):
        """Gets all server sockets that exist in the process."""

    def GetChannel(self, request, context):
        """Returns a single Channel, or else a NOT_FOUND code."""

    def GetSubchannel(self, request, context):
        """Returns a single Subchannel, or else a NOT_FOUND code."""

    def GetSocket(self, request, context):
        """Returns a single Socket or else a NOT_FOUND code."""

def add_ChannelzServicer_to_server(servicer, server) -> None: ...

class Channelz:
    """Channelz is a service exposed by gRPC servers that provides detailed debug
    information.
    """

    @staticmethod
    def GetTopChannels(
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
    def GetServers(
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
    def GetServer(
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
    def GetServerSockets(
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
    def GetChannel(
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
    def GetSubchannel(
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
    def GetSocket(
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
