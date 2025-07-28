from ..scope import Scope
from ..scope_manager import ScopeManager
from ..span import Span

class ThreadLocalScopeManager(ScopeManager):
    """
    :class:`~opentracing.ScopeManager` implementation that stores the
    current active :class:`~opentracing.Scope` using thread-local storage.
    """

    def __init__(self) -> None: ...
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
        can be used to access the currently active
        :attr:`Scope.span`.

        :return: the :class:`~opentracing.Scope` that is active,
            or ``None`` if not available.
        """
