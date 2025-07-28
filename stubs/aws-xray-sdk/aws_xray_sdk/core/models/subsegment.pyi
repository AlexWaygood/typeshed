from _typeshed import Incomplete
from types import TracebackType
from typing import Final

from ..recorder import AWSXRayRecorder
from .dummy_entities import DummySubsegment
from .entity import Entity
from .segment import Segment

SUBSEGMENT_RECORDING_ATTRIBUTE: Final[str]

def set_as_recording(decorated_func, wrapped) -> None: ...
def is_already_recording(func): ...
def subsegment_decorator(wrapped, instance, args, kwargs): ...

class SubsegmentContextManager:
    """
    Wrapper for segment and recorder to provide segment context manager.
    """

    name: str | None
    subsegment_kwargs: dict[str, str]
    recorder: AWSXRayRecorder
    subsegment: Subsegment | None
    def __init__(self, recorder: AWSXRayRecorder, name: str | None = None, *, namespace: str = "local") -> None: ...
    def __call__(self, wrapped, instance, args: list[Incomplete], kwargs: dict[str, Incomplete]): ...
    def __enter__(self) -> DummySubsegment | Subsegment | None: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

class Subsegment(Entity):
    """
    The work done in a single segment can be broke down into subsegments.
    Subsegments provide more granular timing information and details about
    downstream calls that your application made to fulfill the original request.
    A subsegment can contain additional details about a call to an AWS service,
    an external HTTP API, or an SQL database.
    """

    parent_segment: Segment
    trace_id: str
    type: str
    namespace: str
    sql: dict[str, Incomplete]
    def __init__(self, name: str, namespace: str, segment: Segment) -> None:
        """
        Create a new subsegment.

        :param str name: Subsegment name is required.
        :param str namespace: The namespace of the subsegment. Currently
            support `aws`, `remote` and `local`.
        :param Segment segment: The parent segment
        """

    def add_subsegment(self, subsegment: Subsegment) -> None:
        """
        Add input subsegment as a child subsegment and increment
        reference counter and total subsegments counter of the
        parent segment.
        """

    def remove_subsegment(self, subsegment: Subsegment) -> None:
        """
        Remove input subsegment from child subsegemnts and
        decrement parent segment total subsegments count.

        :param Subsegment: subsegment to remove.
        """

    def close(self, end_time: float | None = None) -> None:
        """
        Close the trace entity by setting `end_time`
        and flip the in progress flag to False. Also decrement
        parent segment's ref counter by 1.

        :param float end_time: Epoch in seconds. If not specified
            current time will be used.
        """

    def set_sql(self, sql: dict[str, Incomplete]) -> None:
        """
        Set sql related metadata. This function is used by patchers
        for database connectors and is not recommended to
        invoke manually.

        :param dict sql: sql related metadata
        """

    def to_dict(self) -> dict[str, Incomplete]:
        """
        Convert Subsegment object to dict with required properties
        that have non-empty values.
        """
