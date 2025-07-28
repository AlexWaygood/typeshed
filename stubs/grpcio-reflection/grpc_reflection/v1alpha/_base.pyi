"""Base implementation of reflection servicer."""

from grpc_reflection.v1alpha import reflection_pb2_grpc

class BaseReflectionServicer(reflection_pb2_grpc.ServerReflectionServicer):
    """Base class for reflection servicer."""

    def __init__(self, service_names, pool=None) -> None:
        """Constructor.

        Args:
            service_names: Iterable of fully-qualified service names available.
            pool: An optional DescriptorPool instance.
        """

__all__ = ["BaseReflectionServicer"]
