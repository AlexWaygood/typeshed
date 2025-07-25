from _typeshed import Incomplete
from logging import Logger
from traceback import StackSummary
from typing import Any, Final, Literal, overload

from .subsegment import Subsegment
from .throwable import Throwable

log: Logger
ORIGIN_TRACE_HEADER_ATTR_KEY: Final[str]

class Entity:
    """
    The parent class for segment/subsegment. It holds common properties
    and methods on segment and subsegment.
    """

    id: str
    name: str
    start_time: float
    parent_id: str | None
    sampled: bool
    in_progress: bool
    http: dict[str, dict[str, str | int]]
    annotations: dict[str, float | str | bool]
    metadata: dict[str, dict[str, Any]]  # value is any object that can be serialized into JSON string
    aws: dict[str, Incomplete]
    cause: dict[str, str | list[Throwable]]
    subsegments: list[Subsegment]
    end_time: float
    def __init__(self, name: str, entity_id: str | None = None) -> None: ...
    def close(self, end_time: float | None = None) -> None:
        """
        Close the trace entity by setting `end_time`
        and flip the in progress flag to False.

        :param float end_time: Epoch in seconds. If not specified
            current time will be used.
        """

    def add_subsegment(self, subsegment: Subsegment) -> None:
        """
        Add input subsegment as a child subsegment.
        """

    def remove_subsegment(self, subsegment: Subsegment) -> None:
        """
        Remove input subsegment from child subsegments.
        """

    @overload
    def put_http_meta(self, key: Literal["status", "content_length"], value: int) -> None:
        """
        Add http related metadata.

        :param str key: Currently supported keys are:
            * url
            * method
            * user_agent
            * client_ip
            * status
            * content_length
        :param value: status and content_length are int and for other
            supported keys string should be used.
        """

    @overload
    def put_http_meta(self, key: Literal["url", "method", "user_agent", "client_ip", "x_forwarded_for"], value: str) -> None: ...
    def put_annotation(self, key: str, value: float | str | bool) -> None:
        """
        Annotate segment or subsegment with a key-value pair.
        Annotations will be indexed for later search query.

        :param str key: annotation key
        :param object value: annotation value. Any type other than
            string/number/bool will be dropped
        """

    def put_metadata(
        self, key: str, value: Any, namespace: str = "default"  # value is any object that can be serialized into JSON string
    ) -> None:
        """
        Add metadata to segment or subsegment. Metadata is not indexed
        but can be later retrieved by BatchGetTraces API.

        :param str namespace: optional. Default namespace is `default`.
            It must be a string and prefix `AWS.` is reserved.
        :param str key: metadata key under specified namespace
        :param object value: any object that can be serialized into JSON string
        """

    def set_aws(self, aws_meta) -> None:
        """
        set aws section of the entity.
        This method is called by global recorder and botocore patcher
        to provide additonal information about AWS runtime.
        It is not recommended to manually set aws section.
        """
    throttle: bool
    def add_throttle_flag(self) -> None: ...
    fault: bool
    def add_fault_flag(self) -> None: ...
    error: bool
    def add_error_flag(self) -> None: ...
    def apply_status_code(self, status_code: int | None) -> None:
        """
        When a trace entity is generated under the http context,
        the status code will affect this entity's fault/error/throttle flags.
        Flip these flags based on status code.
        """

    def add_exception(self, exception: Exception, stack: StackSummary, remote: bool = False) -> None:
        """
        Add an exception to trace entities.

        :param Exception exception: the caught exception.
        :param list stack: the output from python built-in
            `traceback.extract_stack()`.
        :param bool remote: If False it means it's a client error
            instead of a downstream service.
        """

    def save_origin_trace_header(self, trace_header) -> None:
        """
        Temporarily store additional data fields in trace header
        to the entity for later propagation. The data will be
        cleaned up upon serialization.
        """

    def get_origin_trace_header(self):
        """
        Retrieve saved trace header data.
        """

    def serialize(self) -> str:
        """
        Serialize to JSON document that can be accepted by the
        X-Ray backend service. It uses json to perform serialization.
        """

    def to_dict(self) -> dict[str, Incomplete]:
        """
        Convert Entity(Segment/Subsegment) object to dict
        with required properties that have non-empty values.
        """
