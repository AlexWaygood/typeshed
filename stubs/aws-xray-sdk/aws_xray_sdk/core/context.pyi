import time
from logging import Logger
from typing import Any

from .models.entity import Entity
from .models.segment import Segment
from .models.subsegment import Subsegment

log: Logger
SUPPORTED_CONTEXT_MISSING: Any
MISSING_SEGMENT_MSG: str
CXT_MISSING_STRATEGY_KEY: str

class Context:
    """
    The context storage class to store trace entities(segments/subsegments).
    The default implementation uses threadlocal to store these entities.
    It also provides interfaces to manually inject trace entities which will
    replace the current stored entities and to clean up the storage.

    For any data access or data mutation, if there is no active segment present
    if will use user-defined behavior to handle such case. By default it throws
    an runtime error.

    This data structure is thread-safe.
    """

    def __init__(self, context_missing: str = "LOG_ERROR") -> None: ...
    def put_segment(self, segment: Segment) -> None:
        """
        Store the segment created by ``xray_recorder`` to the context.
        It overrides the current segment if there is already one.
        """

    def end_segment(self, end_time: time.struct_time | None = None) -> None:
        """
        End the current active segment.

        :param float end_time: epoch in seconds. If not specified the current
            system time will be used.
        """

    def put_subsegment(self, subsegment: Subsegment) -> None:
        """
        Store the subsegment created by ``xray_recorder`` to the context.
        If you put a new subsegment while there is already an open subsegment,
        the new subsegment becomes the child of the existing subsegment.
        """

    def end_subsegment(self, end_time: time.struct_time | None = None):
        """
        End the current active segment. Return False if there is no
        subsegment to end.

        :param float end_time: epoch in seconds. If not specified the current
            system time will be used.
        """

    def get_trace_entity(self):
        """
        Return the current trace entity(segment/subsegment). If there is none,
        it behaves based on pre-defined ``context_missing`` strategy.
        If the SDK is disabled, returns a DummySegment
        """

    def set_trace_entity(self, trace_entity: Entity) -> None:
        """
        Store the input trace_entity to local context. It will overwrite all
        existing ones if there is any.
        """

    def clear_trace_entities(self) -> None:
        """
        clear all trace_entities stored in the local context.
        In case of using threadlocal to store trace entites, it will
        clean up all trace entities created by the current thread.
        """

    def handle_context_missing(self) -> None:
        """
        Called whenever there is no trace entity to access or mutate.
        """

    @property
    def context_missing(self): ...
    @context_missing.setter
    def context_missing(self, value: str) -> None: ...
