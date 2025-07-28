from typing_extensions import Self

import opentracing

class SpanContext(opentracing.SpanContext):
    """SpanContext satisfies the opentracing.SpanContext contract.

    trace_id and span_id are uint64's, so their range is [1, 2^64).
    """

    trace_id: int | None
    span_id: int | None
    def __init__(
        self, trace_id: int | None = None, span_id: int | None = None, baggage: dict[str, str] | None = None
    ) -> None: ...
    @property
    def baggage(self) -> dict[str, str]: ...
    def with_baggage_item(self, key: str, value: str) -> Self: ...
