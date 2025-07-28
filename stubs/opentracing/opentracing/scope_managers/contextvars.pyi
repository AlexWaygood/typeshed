from ..scope import Scope
from ..scope_manager import ScopeManager
from ..span import Span

class ContextVarsScopeManager(ScopeManager):
    """
    :class:`~opentracing.ScopeManager` implementation for **asyncio**
    that stores the :class:`~opentracing.Scope` using ContextVar.

    The scope manager provides automatic :class:`~opentracing.Span` propagation
    from parent coroutines, tasks and scheduled in event loop callbacks to
    their children.

    .. code-block:: python

        async def child_coroutine():
            # No need manual activation of parent span in child coroutine.
            with tracer.start_active_span('child') as scope:
                ...

        async def parent_coroutine():
            with tracer.start_active_span('parent') as scope:
                ...
                await child_coroutine()
                ...

    """

    def activate(self, span: Span, finish_on_close: bool) -> Scope:
        """
        Make a :class:`~opentracing.Span` instance active.

        :param span: the :class:`~opentracing.Span` that should become active.
        :param finish_on_close: whether *span* should automatically be
            finished when :meth:`Scope.close()` is called.

        :return: a :class:`~opentracing.Scope` instance to control the end
            of the active period for the :class:`~opentracing.Span`.
            It is a programming error to neglect to call :meth:`Scope.close()`
            on the returned instance.
        """

    @property
    def active(self) -> Scope:
        """
        Return the currently active :class:`~opentracing.Scope` which
        can be used to access the currently active :attr:`Scope.span`.

        :return: the :class:`~opentracing.Scope` that is active,
            or ``None`` if not available.
        """

def no_parent_scope() -> None:
    """
    Context manager that resets current Scope. Intended to break span
    propagation to children coroutines, tasks or scheduled callbacks.

    .. code-block:: python

        from opentracing.scope_managers.contextvars import no_parent_scope

        def periodic()
            # `periodic` span will be children of root only at the first time.
            with self.tracer.start_active_span('periodic'):
                # Now we break span propagation.
                with no_parent_scope():
                    self.loop.call_soon(periodic)

        with self.tracer.start_active_span('root'):
            self.loop.call_soon(periodic)
    """
