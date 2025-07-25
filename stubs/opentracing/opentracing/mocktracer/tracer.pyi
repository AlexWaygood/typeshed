from typing import Any

from ..scope_manager import ScopeManager
from ..span import Span
from ..tracer import Reference, Tracer
from .context import SpanContext
from .propagator import Propagator
from .span import MockSpan

class MockTracer(Tracer):
    """MockTracer makes it easy to test the semantics of OpenTracing
    instrumentation.

    By using a MockTracer as a :class:`~opentracing.Tracer` implementation
    for tests, a developer can assert that :class:`~opentracing.Span`
    properties and relationships with other
    **Spans** are defined as expected by instrumentation code.

    By default, MockTracer registers propagators for :attr:`Format.TEXT_MAP`,
    :attr:`Format.HTTP_HEADERS` and :attr:`Format.BINARY`. The user should
    call :func:`register_propagator()` for each additional inject/extract
    format.
    """

    def __init__(self, scope_manager: ScopeManager | None = None) -> None:
        """Initialize a MockTracer instance."""

    @property
    def active_span(self) -> MockSpan | None:
        """Provides access to the the active :class:`Span`. This is a shorthand for
        :attr:`Tracer.scope_manager.active.span`, and ``None`` will be
        returned if :attr:`Scope.span` is ``None``.

        :rtype: :class:`~opentracing.Span`
        :return: the active :class:`Span`.
        """

    def register_propagator(self, format: str, propagator: Propagator) -> None:
        """Register a propagator with this MockTracer.

        :param string format: a :class:`~opentracing.Format`
            identifier like :attr:`~opentracing.Format.TEXT_MAP`
        :param **Propagator** propagator: a **Propagator** instance to handle
            inject/extract calls involving `format`
        """

    def finished_spans(self) -> list[MockSpan]:
        """Return a copy of all finished **Spans** started by this MockTracer
        (since construction or the last call to :meth:`~MockTracer.reset()`)

        :rtype: list
        :return: a copy of the finished **Spans**.
        """

    def reset(self) -> None:
        """Clear the finished **Spans** queue.

        Note that this does **not** have any effect on **Spans** created by
        MockTracer that have not finished yet; those
        will still be enqueued in :meth:`~MockTracer.finished_spans()`
        when they :func:`finish()`.
        """

    def start_span(  # type: ignore[override]
        self,
        operation_name: str | None = None,
        child_of: Span | SpanContext | None = None,
        references: list[Reference] | None = None,
        tags: dict[Any, Any] | None = None,
        start_time: float | None = None,
        ignore_active_span: bool = False,
    ) -> MockSpan: ...
    def extract(self, format: str, carrier: dict[Any, Any]) -> SpanContext: ...
