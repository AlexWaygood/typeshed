from .scope import Scope
from .span import Span

class ScopeManager:
    """The :class:`ScopeManager` interface abstracts both the activation of
    a :class:`Span` and access to an active :class:`Span`/:class:`Scope`.
    """

    def __init__(self) -> None: ...
    def activate(self, span: Span, finish_on_close: bool) -> Scope:
        """Makes a :class:`Span` active.

        :param span: the :class:`Span` that should become active.
        :param finish_on_close: whether :class:`Span` should be automatically
            finished when :meth:`Scope.close()` is called.

        :rtype: Scope
        :return: a :class:`Scope` to control the end of the active period for
            *span*. It is a programming error to neglect to call
            :meth:`Scope.close()` on the returned instance.
        """

    @property
    def active(self) -> Scope | None:
        """Returns the currently active :class:`Scope` which can be used to access the
        currently active :attr:`Scope.span`.

        If there is a non-null :class:`Scope`, its wrapped :class:`Span`
        becomes an implicit parent of any newly-created :class:`Span` at
        :meth:`Tracer.start_active_span()` time.

        :rtype: Scope
        :return: the :class:`Scope` that is active, or ``None`` if not
            available.
        """
