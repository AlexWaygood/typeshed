"""The AsyncIO version of the reflection servicer."""

from collections.abc import AsyncIterable

from grpc_reflection.v1alpha import reflection_pb2
from grpc_reflection.v1alpha._base import BaseReflectionServicer

class ReflectionServicer(BaseReflectionServicer):
    """Servicer handling RPCs for service statuses."""

    async def ServerReflectionInfo(
        self, request_iterator: AsyncIterable[reflection_pb2.ServerReflectionRequest], unused_context
    ) -> AsyncIterable[reflection_pb2.ServerReflectionResponse]: ...

__all__ = ["ReflectionServicer"]
