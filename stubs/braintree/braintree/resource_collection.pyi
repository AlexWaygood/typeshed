from _typeshed import Incomplete
from collections.abc import Generator

class ResourceCollection:
    """
    A class representing results from a search. Supports the iterator protocol::

        results = braintree.Transaction.search("411111")
        for transaction in results:
            print transaction.id
    """

    def __init__(self, query, results, method) -> None: ...
    @property
    def maximum_size(self):
        """
        Returns the approximate size of the results.  The size is approximate due to race conditions when pulling
        back results.  Due to its inexact nature, maximum_size should be avoided.
        """

    @property
    def first(self):
        """Returns the first item in the results."""

    @property
    def items(self) -> Generator[Incomplete, None, None]:
        """Returns a generator allowing iteration over all of the results."""

    @property
    def ids(self):
        """Returns the list of ids in the search result."""

    def __iter__(self): ...
