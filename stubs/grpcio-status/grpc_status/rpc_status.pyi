"""Reference implementation for status mapping in gRPC Python."""

import grpc

from . import _async as aio

# Returns a google.rpc.status.Status message corresponding to a given grpc.Call.
def from_call(call: grpc.Call):
    """Returns a google.rpc.status.Status message corresponding to a given grpc.Call.

    This is an EXPERIMENTAL API.

    Args:
      call: A grpc.Call instance.

    Returns:
      A google.rpc.status.Status message representing the status of the RPC.

    Raises:
      ValueError: If the gRPC call's code or details are inconsistent with the
        status code and message inside of the google.rpc.status.Status.
    """

# Convert a google.rpc.status.Status message to grpc.Status.
def to_status(status) -> grpc.Status:
    """Convert a google.rpc.status.Status message to grpc.Status.

    This is an EXPERIMENTAL API.

    Args:
      status: a google.rpc.status.Status message representing the non-OK status
        to terminate the RPC with and communicate it to the client.

    Returns:
      A grpc.Status instance representing the input google.rpc.status.Status message.
    """

__all__ = ["from_call", "to_status", "aio"]
