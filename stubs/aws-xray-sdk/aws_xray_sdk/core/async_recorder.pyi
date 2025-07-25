from types import TracebackType

from .models.segment import SegmentContextManager
from .models.subsegment import SubsegmentContextManager
from .recorder import AWSXRayRecorder

class AsyncSegmentContextManager(SegmentContextManager):
    async def __aenter__(self): ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

class AsyncSubsegmentContextManager(SubsegmentContextManager):
    async def __call__(self, wrapped, instance, args, kwargs): ...
    async def __aenter__(self): ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

class AsyncAWSXRayRecorder(AWSXRayRecorder):
    def capture_async(self, name=None):
        """
        A decorator that records enclosed function in a subsegment.
        It only works with asynchronous functions.

        params str name: The name of the subsegment. If not specified
        the function name will be used.
        """

    def in_segment_async(self, name=None, **segment_kwargs):
        """
        Return a segment async context manager.

        :param str name: the name of the segment
        :param dict segment_kwargs: remaining arguments passed directly to `begin_segment`
        """

    def in_subsegment_async(self, name=None, **subsegment_kwargs):
        """
        Return a subsegment async context manager.

        :param str name: the name of the segment
        :param dict segment_kwargs: remaining arguments passed directly to `begin_segment`
        """

    async def record_subsegment_async(self, wrapped, instance, args, kwargs, name, namespace, meta_processor): ...
