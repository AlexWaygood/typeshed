from types import TracebackType
from typing_extensions import Self

from .scope_manager import ScopeManager
from .span import Span

class Scope:
    """A scope formalizes the activation and deactivation of a :class:`Span`,
    usually from a CPU standpoint. Many times a :class:`Span` will be extant
    (in that :meth:`Span.finish()` has not been called) despite being in a
    non-runnable state from a CPU/scheduler standpoint. For instance, a
    :class:`Span` representing the client side of an RPC will be unfinished but
    blocked on IO while the RPC is still outstanding. A scope defines when a
    given :class:`Span` is scheduled and on the path.

    :param manager: the :class:`ScopeManager` that created this :class:`Scope`.
    :type manager: ScopeManager

    :param span: the :class:`Span` used for this :class:`Scope`.
    :type span: Span
    """

    def __init__(self, manager: ScopeManager, span: Span) -> None:
        """Initializes a scope for *span*."""

    @property
    def span(self) -> Span:
        """Returns the :class:`Span` wrapped by this :class:`Scope`.

        :rtype: Span
        """

    @property
    def manager(self) -> ScopeManager:
        """Returns the :class:`ScopeManager` that created this :class:`Scope`.

        :rtype: ScopeManager
        """

    def close(self) -> None:
        """Marks the end of the active period for this :class:`Scope`, updating
        :attr:`ScopeManager.active` in the process.

        NOTE: Calling this method more than once on a single :class:`Scope`
        leads to undefined behavior.
        """

    def __enter__(self) -> Self:
        """Allows :class:`Scope` to be used inside a Python Context Manager."""

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Calls :meth:`close()` when the execution is outside the Python
        Context Manager.

        If exception has occurred during execution, it is automatically logged
        and added as a tag to the :class:`Span`.
        :attr:`~operation.ext.tags.ERROR` will also be set to `True`.
        """
