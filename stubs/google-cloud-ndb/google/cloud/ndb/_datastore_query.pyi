"""Translate NDB queries to Datastore calls."""

from _typeshed import Incomplete
from typing import Any

class QueryIterator:
    """An iterator for query results.

    Executes the given query and provides an interface for iterating over
    instances of either :class:`model.Model` or :class:`key.Key` depending on
    whether ``keys_only`` was specified for the query.

    This is an abstract base class. Users should not instantiate an iterator
    class directly. Use :meth:`query.Query.iter` or ``iter(query)`` to get an
    instance of :class:`QueryIterator`.
    """

    def __iter__(self): ...
    def has_next(self) -> None:
        """Is there at least one more result?

        Blocks until the answer to this question is known and buffers the
        result (if any) until retrieved with :meth:`next`.

        Returns:
            bool: :data:`True` if a subsequent call to
                :meth:`QueryIterator.next` will return a result, otherwise
                :data:`False`.
        """

    def has_next_async(self) -> None:
        """Asynchronous version of :meth:`has_next`.

        Returns:
            tasklets.Future: See :meth:`has_next`.
        """

    def probably_has_next(self) -> None:
        """Like :meth:`has_next` but won't block.

        This uses a (sometimes inaccurate) shortcut to avoid having to hit the
        Datastore for the answer.

        May return a false positive (:data:`True` when :meth:`next` would
        actually raise ``StopIteration``), but never a false negative
        (:data:`False` when :meth:`next` would actually return a result).
        """

    def next(self) -> None:
        """Get the next result.

        May block. Guaranteed not to block if immediately following a call to
        :meth:`has_next` or :meth:`has_next_async` which will buffer the next
        result.

        Returns:
            Union[model.Model, key.Key]: Depending on if ``keys_only=True`` was
                passed in as an option.
        """

    def cursor_before(self) -> None:
        """Get a cursor to the point just before the last result returned.

        Returns:
            Cursor: The cursor.

        Raises:
            exceptions.BadArgumentError: If there is no cursor to return. This
                will happen if the iterator hasn't returned a result yet, has
                only returned a single result so far, or if the iterator has
                been exhausted. Also, if query uses ``OR``, ``!=``, or ``IN``,
                since those are composites of multiple Datastore queries each
                with their own cursors—it is impossible to return a cursor for
                the composite query.
        """

    def cursor_after(self) -> None:
        """Get a cursor to the point just after the last result returned.

        Returns:
            Cursor: The cursor.

        Raises:
            exceptions.BadArgumentError: If there is no cursor to return. This
                will happen if the iterator hasn't returned a result yet. Also,
                if query uses ``OR``, ``!=``, or ``IN``, since those are
                composites of multiple Datastore queries each with their own
                cursors—it is impossible to return a cursor for the composite
                query.
        """

    def index_list(self) -> None:
        """Return a list of indexes used by the query.

        Raises:
            NotImplementedError: Always. This information is no longer
                available from query results in Datastore.
        """

class Cursor:
    """Cursor.

    A pointer to a place in a sequence of query results. Cursor itself is just
    a byte sequence passed back by Datastore. This class wraps that with
    methods to convert to/from a URL safe string.

    API for converting to/from a URL safe string is different depending on
    whether you're reading the Legacy NDB docstrings or the official Legacy NDB
    documentation on the web. We do both here.

    Args:
        cursor (bytes): Raw cursor value from Datastore
    """

    @classmethod
    def from_websafe_string(cls, urlsafe): ...
    cursor: Any
    def __init__(self, cursor: Incomplete | None = ..., urlsafe: Incomplete | None = ...) -> None: ...
    def to_websafe_string(self): ...
    def urlsafe(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self) -> int: ...
