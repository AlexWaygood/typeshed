import time
from _typeshed import FileDescriptorOrPath
from collections.abc import Callable, Iterable
from logging import Logger
from typing import Any

from .context import Context
from .emitters.udp_emitter import UDPEmitter
from .models.default_dynamic_naming import DefaultDynamicNaming
from .models.dummy_entities import DummySegment, DummySubsegment
from .models.segment import Segment, SegmentContextManager
from .models.subsegment import Subsegment, SubsegmentContextManager
from .sampling.local.sampler import LocalSampler
from .sampling.sampler import DefaultSampler
from .streaming.default_streaming import DefaultStreaming

log: Logger
TRACING_NAME_KEY: str
DAEMON_ADDR_KEY: str
CONTEXT_MISSING_KEY: str
XRAY_META: dict[str, dict[str, str]]
SERVICE_INFO: dict[str, str]

class AWSXRayRecorder:
    """
    A global AWS X-Ray recorder that will begin/end segments/subsegments
    and send them to the X-Ray daemon. This recorder is initialized during
    loading time so you can use::

        from aws_xray_sdk.core import xray_recorder

    in your module to access it
    """

    def __init__(self) -> None: ...
    def configure(
        self,
        sampling: bool | None = None,
        plugins: Iterable[str] | None = None,
        context_missing: str | None = None,
        sampling_rules: dict[str, Any] | FileDescriptorOrPath | None = None,
        daemon_address: str | None = None,
        service: str | None = None,
        context: Context | None = None,
        emitter: UDPEmitter | None = None,
        streaming: DefaultStreaming | None = None,
        dynamic_naming: DefaultDynamicNaming | None = None,
        streaming_threshold: int | None = None,
        max_trace_back: int | None = None,
        sampler: LocalSampler | DefaultSampler | None = None,
        stream_sql: bool | None = True,
    ) -> None:
        """Configure global X-Ray recorder.

        Configure needs to run before patching thrid party libraries
        to avoid creating dangling subsegment.

        :param bool sampling: If sampling is enabled, every time the recorder
            creates a segment it decides whether to send this segment to
            the X-Ray daemon. This setting is not used if the recorder
            is running in AWS Lambda. The recorder always respect the incoming
            sampling decisions regardless of this setting.
        :param sampling_rules: Pass a set of local custom sampling rules.
            Can be an absolute path of the sampling rule config json file
            or a dictionary that defines those rules. This will also be the
            fallback rules in case of centralized sampling opted-in while
            the cetralized sampling rules are not available.
        :param sampler: The sampler used to make sampling decisions. The SDK
            provides two built-in samplers. One is centralized rules based and
            the other is local rules based. The former is the default.
        :param tuple plugins: plugins that add extra metadata to each segment.
            Currently available plugins are EC2Plugin, ECS plugin and
            ElasticBeanstalkPlugin.
            If you want to disable all previously enabled plugins,
            pass an empty tuple ``()``.
        :param str context_missing: recorder behavior when it tries to mutate
            a segment or add a subsegment but there is no active segment.
            RUNTIME_ERROR means the recorder will raise an exception.
            LOG_ERROR means the recorder will only log the error and
            do nothing.
            IGNORE_ERROR means the recorder will do nothing
        :param str daemon_address: The X-Ray daemon address where the recorder
            sends data to.
        :param str service: default segment name if creating a segment without
            providing a name.
        :param context: You can pass your own implementation of context storage
            for active segment/subsegment by overriding the default
            ``Context`` class.
        :param emitter: The emitter that sends a segment/subsegment to
            the X-Ray daemon. You can override ``UDPEmitter`` class.
        :param dynamic_naming: a string that defines a pattern that host names
            should match. Alternatively you can pass a module which
            overrides ``DefaultDynamicNaming`` module.
        :param streaming: The streaming module to stream out trace documents
            when they grow too large. You can override ``DefaultStreaming``
            class to have your own implementation of the streaming process.
        :param streaming_threshold: If breaks within a single segment it will
            start streaming out children subsegments. By default it is the
            maximum number of subsegments within a segment.
        :param int max_trace_back: The maxinum number of stack traces recorded
            by auto-capture. Lower this if a single document becomes too large.
        :param bool stream_sql: Whether SQL query texts should be streamed.

        Environment variables AWS_XRAY_DAEMON_ADDRESS, AWS_XRAY_CONTEXT_MISSING
        and AWS_XRAY_TRACING_NAME respectively overrides arguments
        daemon_address, context_missing and service.
        """

    def in_segment(self, name: str | None = None, **segment_kwargs) -> SegmentContextManager:
        """
        Return a segment context manager.

        :param str name: the name of the segment
        :param dict segment_kwargs: remaining arguments passed directly to `begin_segment`
        """

    def in_subsegment(self, name: str | None = None, **subsegment_kwargs) -> SubsegmentContextManager:
        """
        Return a subsegment context manager.

        :param str name: the name of the subsegment
        :param dict subsegment_kwargs: remaining arguments passed directly to `begin_subsegment`
        """

    def begin_segment(
        self, name: str | None = None, traceid: str | None = None, parent_id: str | None = None, sampling: bool | None = None
    ) -> Segment | DummySegment:
        """
        Begin a segment on the current thread and return it. The recorder
        only keeps one segment at a time. Create the second one without
        closing existing one will overwrite it.

        :param str name: the name of the segment
        :param str traceid: trace id of the segment
        :param int sampling: 0 means not sampled, 1 means sampled
        """

    def end_segment(self, end_time: time.struct_time | None = None) -> None:
        """
        End the current segment and send it to X-Ray daemon
        if it is ready to send. Ready means segment and
        all its subsegments are closed.

        :param float end_time: segment completion in unix epoch in seconds.
        """

    def current_segment(self) -> Segment:
        """
        Return the currently active segment. In a multithreading environment,
        this will make sure the segment returned is the one created by the
        same thread.
        """

    def begin_subsegment(self, name: str, namespace: str = "local") -> DummySubsegment | Subsegment | None:
        """
        Begin a new subsegment.
        If there is open subsegment, the newly created subsegment will be the
        child of latest opened subsegment.
        If not, it will be the child of the current open segment.

        :param str name: the name of the subsegment.
        :param str namespace: currently can only be 'local', 'remote', 'aws'.
        """

    def begin_subsegment_without_sampling(self, name: str) -> DummySubsegment | Subsegment | None:
        """
        Begin a new unsampled subsegment.
        If there is open subsegment, the newly created subsegment will be the
        child of latest opened subsegment.
        If not, it will be the child of the current open segment.

        :param str name: the name of the subsegment.
        """

    def current_subsegment(self) -> Subsegment | DummySubsegment | None:
        """
        Return the latest opened subsegment. In a multithreading environment,
        this will make sure the subsegment returned is one created
        by the same thread.
        """

    def end_subsegment(self, end_time: time.struct_time | None = None) -> None:
        """
        End the current active subsegment. If this is the last one open
        under its parent segment, the entire segment will be sent.

        :param float end_time: subsegment compeletion in unix epoch in seconds.
        """

    def put_annotation(self, key: str, value: Any) -> None:
        """
        Annotate current active trace entity with a key-value pair.
        Annotations will be indexed for later search query.

        :param str key: annotation key
        :param object value: annotation value. Any type other than
            string/number/bool will be dropped
        """

    def put_metadata(self, key: str, value: Any, namespace: str = "default") -> None:
        """
        Add metadata to the current active trace entity.
        Metadata is not indexed but can be later retrieved
        by BatchGetTraces API.

        :param str namespace: optional. Default namespace is `default`.
            It must be a string and prefix `AWS.` is reserved.
        :param str key: metadata key under specified namespace
        :param object value: any object that can be serialized into JSON string
        """

    def is_sampled(self) -> bool:
        """
        Check if the current trace entity is sampled or not.
        Return `False` if no active entity found.
        """

    def get_trace_entity(self) -> Segment | Subsegment | DummySegment | DummySubsegment:
        """
        A pass through method to ``context.get_trace_entity()``.
        """

    def set_trace_entity(self, trace_entity: Segment | Subsegment | DummySegment | DummySubsegment) -> None:
        """
        A pass through method to ``context.set_trace_entity()``.
        """

    def clear_trace_entities(self) -> None:
        """
        A pass through method to ``context.clear_trace_entities()``.
        """

    def stream_subsegments(self) -> None:
        """
        Stream all closed subsegments to the daemon
        and remove reference to the parent segment.
        No-op for a not sampled segment.
        """

    def capture(self, name: str | None = None) -> SubsegmentContextManager:
        """
        A decorator that records enclosed function in a subsegment.
        It only works with synchronous functions.

        params str name: The name of the subsegment. If not specified
        the function name will be used.
        """

    def record_subsegment(
        self,
        wrapped: Callable[..., Any],
        instance: Any,
        args: list[Any],
        kwargs: dict[str, Any],
        name: str,
        namespace: str,
        meta_processor: Callable[..., object],
    ) -> Any: ...
    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def sampling(self) -> bool: ...
    @sampling.setter
    def sampling(self, value: bool) -> None: ...
    @property
    def sampler(self) -> LocalSampler | DefaultSampler: ...
    @sampler.setter
    def sampler(self, value: LocalSampler | DefaultSampler) -> None: ...
    @property
    def service(self) -> str: ...
    @service.setter
    def service(self, value: str) -> None: ...
    @property
    def dynamic_naming(self) -> DefaultDynamicNaming | None: ...
    @dynamic_naming.setter
    def dynamic_naming(self, value: DefaultDynamicNaming | str) -> None: ...
    @property
    def context(self) -> Context: ...
    @context.setter
    def context(self, cxt: Context) -> None: ...
    @property
    def emitter(self) -> UDPEmitter: ...
    @emitter.setter
    def emitter(self, value: UDPEmitter) -> None: ...
    @property
    def streaming(self) -> DefaultStreaming: ...
    @streaming.setter
    def streaming(self, value: DefaultStreaming) -> None: ...
    @property
    def streaming_threshold(self) -> int:
        """
        Proxy method to Streaming module's `streaming_threshold` property.
        """

    @streaming_threshold.setter
    def streaming_threshold(self, value: int) -> None: ...
    @property
    def max_trace_back(self) -> int: ...
    @max_trace_back.setter
    def max_trace_back(self, value: int) -> None: ...
    @property
    def stream_sql(self) -> bool: ...
    @stream_sql.setter
    def stream_sql(self, value: bool) -> None: ...
