from ..scope import Scope
from ..scope_managers import ThreadLocalScopeManager
from ..span import Span

class AsyncioScopeManager(ThreadLocalScopeManager):
    """
    :class:`~opentracing.ScopeManager` implementation for **asyncio**
    that stores the :class:`~opentracing.Scope` in the current
    :class:`Task` (:meth:`asyncio.current_task()`), falling back to
    thread-local storage if none was being executed.

    Automatic :class:`~opentracing.Span` propagation from
    parent coroutines to their children is not provided, which needs to be
    done manually:

    .. code-block:: python

        async def child_coroutine(span):
            # activate the parent Span, but do not finish it upon
            # deactivation. That will be done by the parent coroutine.
            with tracer.scope_manager.activate(span, finish_on_close=False):
                with tracer.start_active_span('child') as scope:
                    ...

        async def parent_coroutine():
            with tracer.start_active_span('parent') as scope:
                ...
                await child_coroutine(span)
                ...

    """

    def activate(self, span: Span, finish_on_close: bool) -> Scope:
        """
        Make a :class:`~opentracing.Span` instance active.

        :param span: the :class:`~opentracing.Span` that should become active.
        :param finish_on_close: whether *span* should automatically be
            finished when :meth:`Scope.close()` is called.

        If no :class:`Task` is being executed, thread-local
        storage will be used to store the :class:`~opentracing.Scope`.

        :return: a :class:`~opentracing.Scope` instance to control the end
            of the active period for the :class:`~opentracing.Span`.
            It is a programming error to neglect to call :meth:`Scope.close()`
            on the returned instance.
        """

    @property
    def active(self) -> Scope:
        """
        Return the currently active :class:`~opentracing.Scope` which
        can be used to access the currently active
        :attr:`Scope.span`.

        :return: the :class:`~opentracing.Scope` that is active,
            or ``None`` if not available.
        """
