"""Channelz debug service implementation in gRPC Python."""

from grpc_channelz.v1 import _async as aio
from grpc_channelz.v1._servicer import ChannelzServicer

def add_channelz_servicer(server) -> None:
    """Add Channelz servicer to a server.

    Channelz servicer is in charge of
    pulling information from C-Core for entire process. It will allow the
    server to response to Channelz queries.

    The Channelz statistic is enabled by default inside C-Core. Whether the
    statistic is enabled or not is isolated from adding Channelz servicer.
    That means you can query Channelz info with a Channelz-disabled channel,
    and you can add Channelz servicer to a Channelz-disabled server.

    The Channelz statistic can be enabled or disabled by channel option
    'grpc.enable_channelz'. Set to 1 to enable, set to 0 to disable.

    This is an EXPERIMENTAL API.

    Args:
        server: A gRPC server to which Channelz service will be added.
    """

__all__ = ["aio", "add_channelz_servicer", "ChannelzServicer"]
