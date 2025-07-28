"""Reference implementation for status mapping in gRPC Python."""

from _typeshed import Incomplete

async def from_call(call) -> Incomplete | None:
    """Returns a google.rpc.status.Status message from a given grpc.aio.Call.

    This is an EXPERIMENTAL API.

    Args:
      call: An grpc.aio.Call instance.

    Returns:
      A google.rpc.status.Status message representing the status of the RPC.
    """

__all__ = ["from_call"]
