"""Classes representing legacy Google App Engine exceptions.

Unless otherwise noted, these are meant to act as shims for the exception
types defined in the ``google.appengine.api.datastore_errors`` module in
legacy Google App Engine runtime.
"""

from typing import Any

class Error(Exception):
    """Base datastore error type."""

class ContextError(Error):
    """Indicates an NDB call being made without a context.

    Raised whenever an NDB call is made outside of a context
    established by :meth:`google.cloud.ndb.client.Client.context`.
    """

    def __init__(self) -> None: ...

class BadValueError(Error):
    """Indicates a property value or filter value is invalid.

    Raised by ``Entity.__setitem__()``, ``Query.__setitem__()``, ``Get()``,
    and others.
    """

class BadArgumentError(Error):
    """Indicates an invalid argument was passed.

    Raised by ``Query.Order()``, ``Iterator.Next()``, and others.
    """

class BadRequestError(Error):
    """Indicates a bad request was passed.

    Raised by ``Model.non_transactional()`` and others.
    """

class Rollback(Error):
    """Allows a transaction to be rolled back instead of committed.

    Note that *any* exception raised by a transaction function will cause a
    rollback. Hence, this exception type is purely for convenience.
    """

class BadQueryError(Error):
    """Raised by Query when a query or query string is invalid."""

class BadFilterError(Error):
    """Indicates a filter value is invalid.

    Raised by ``Query.__setitem__()`` and ``Query.Run()`` when a filter string
    is invalid.
    """

    filter: Any
    def __init__(self, filter) -> None: ...

class NoLongerImplementedError(NotImplementedError):
    """Indicates a legacy function that is intentionally left unimplemented.

    In the vast majority of cases, this should only be raised by classes,
    functions, or methods that were only been used internally in legacy NDB and
    are no longer necessary because of refactoring. Legacy NDB did a poor job
    of distinguishing between internal and public API. Where we have determined
    that something is probably not a part of the public API, we've removed it
    in order to keep the supported API as clean as possible. It's possible that
    in some cases we've guessed wrong. Get in touch with the NDB development
    team if you think this is the case.
    """

    def __init__(self) -> None: ...

class Cancelled(Error):
    """An operation has been cancelled by user request.

    Raised when trying to get a result from a future that has been cancelled by
    a call to ``Future.cancel`` (possibly on a future that depends on this
    future).
    """

class NestedRetryException(Error):
    """A nested retry block raised an exception.

    Raised when a nested retry block cannot complete due to an exception. This
    allows the outer retry to get back control and retry the whole operation.
    """
