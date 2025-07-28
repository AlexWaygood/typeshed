from _typeshed import Incomplete
from typing import Any

from google.cloud.ndb import tasklets as tasklets

class ContextCache:
    """A per-context in-memory entity cache.

    This cache verifies the fetched entity has the correct key before
    returning a result, in order to handle cases where the entity's key was
    modified but the cache's key was not updated.
    """

    def get_and_validate(self, key):
        """Verify that the entity's key has not changed since it was added
        to the cache. If it has changed, consider this a cache miss.
        See issue 13.  http://goo.gl/jxjOP
        """

class _GlobalCacheBatch:
    """Abstract base for classes used to batch operations for the global cache."""

    def full(self):
        """Indicates whether more work can be added to this batch.

        Returns:
            boolean: `False`, always.
        """

    def idle_callback(self) -> None:
        """Call the cache operation.

        Also, schedule a callback for the completed operation.
        """

    def done_callback(self, cache_call) -> None:
        """Process results of call to global cache.

        If there is an exception for the cache call, distribute that to waiting
        futures, otherwise set the result for all waiting futures to ``None``.
        """

    def make_call(self) -> None:
        """Make the actual call to the global cache. To be overridden."""

    def future_info(self, key) -> None:
        """Generate info string for Future. To be overridden."""

global_get: Any

class _GlobalCacheGetBatch(_GlobalCacheBatch):
    """Batch for global cache get requests.

    Attributes:
        todo (Dict[bytes, List[Future]]): Mapping of keys to futures that are
            waiting on them.

    Arguments:
        ignore_options (Any): Ignored.
    """

    todo: Any
    keys: Any
    def __init__(self, ignore_options) -> None: ...
    def add(self, key):
        """Add a key to get from the cache.

        Arguments:
            key (bytes): The key to get from the cache.

        Returns:
            tasklets.Future: Eventual result will be the entity retrieved from
                the cache (``bytes``) or ``None``.
        """

    def done_callback(self, cache_call) -> None:
        """Process results of call to global cache.

        If there is an exception for the cache call, distribute that to waiting
        futures, otherwise distribute cache hits or misses to their respective
        waiting futures.
        """

    def make_call(self):
        """Call :method:`GlobalCache.get`."""

    def future_info(self, key):
        """Generate info string for Future."""

def global_set(key, value, expires: Incomplete | None = ..., read: bool = ...):
    """Store entity in the global cache.

    Args:
        key (bytes): The key to save.
        value (bytes): The entity to save.
        expires (Optional[float]): Number of seconds until value expires.
        read (bool): Indicates if being set in a read (lookup) context.

    Returns:
        tasklets.Future: Eventual result will be ``None``.
    """

class _GlobalCacheSetBatch(_GlobalCacheBatch):
    """Batch for global cache set requests."""

    expires: Any
    todo: object
    futures: object
    def __init__(self, options) -> None: ...
    def done_callback(self, cache_call) -> None:
        """Process results of call to global cache.

        If there is an exception for the cache call, distribute that to waiting
        futures, otherwise examine the result of the cache call. If the result is
        :data:`None`, simply set the result to :data:`None` for all waiting futures.
        Otherwise, if the result is a `dict`, use that to propagate results for
        individual keys to waiting futures.
        """

    def add(self, key, value):
        """Add a key, value pair to store in the cache.

        Arguments:
            key (bytes): The key to store in the cache.
            value (bytes): The value to store in the cache.

        Returns:
            tasklets.Future: Eventual result will be ``None``.
        """

    def make_call(self):
        """Call :method:`GlobalCache.set`."""

    def future_info(self, key, value):  # type:ignore[override]
        """Generate info string for Future."""

class _GlobalCacheSetIfNotExistsBatch(_GlobalCacheSetBatch):
    """Batch for global cache set_if_not_exists requests."""

    def add(self, key, value):
        """Add a key, value pair to store in the cache.

        Arguments:
            key (bytes): The key to store in the cache.
            value (bytes): The value to store in the cache.

        Returns:
            tasklets.Future: Eventual result will be a ``bool`` value which will be
                :data:`True` if a new value was set for the key, or :data:`False` if a
                value was already set for the key.
        """

    def make_call(self):
        """Call :method:`GlobalCache.set`."""

    def future_info(self, key, value):  # type:ignore[override]
        """Generate info string for Future."""

global_delete: Any

class _GlobalCacheDeleteBatch(_GlobalCacheBatch):
    """Batch for global cache delete requests."""

    keys: Any
    futures: Any
    def __init__(self, ignore_options) -> None: ...
    def add(self, key):
        """Add a key to delete from the cache.

        Arguments:
            key (bytes): The key to delete.

        Returns:
            tasklets.Future: Eventual result will be ``None``.
        """

    def make_call(self):
        """Call :method:`GlobalCache.delete`."""

    def future_info(self, key):
        """Generate info string for Future."""

global_watch: Any

class _GlobalCacheWatchBatch(_GlobalCacheDeleteBatch):
    """Batch for global cache watch requests."""

    def make_call(self):
        """Call :method:`GlobalCache.watch`."""

    def future_info(self, key, value):  # type:ignore[override]
        """Generate info string for Future."""

def global_unwatch(key):
    """End optimistic transaction with global cache.

    Indicates that value for the key wasn't found in the database, so there will not be
    a future call to :func:`global_compare_and_swap`, and we no longer need to watch
    this key.

    Args:
        key (bytes): The key to unwatch.

    Returns:
        tasklets.Future: Eventual result will be ``None``.
    """

class _GlobalCacheUnwatchBatch(_GlobalCacheDeleteBatch):
    """Batch for global cache unwatch requests."""

    def make_call(self):
        """Call :method:`GlobalCache.unwatch`."""

    def future_info(self, key):
        """Generate info string for Future."""

global_compare_and_swap: Any

class _GlobalCacheCompareAndSwapBatch(_GlobalCacheSetBatch):
    """Batch for global cache compare and swap requests."""

    def make_call(self):
        """Call :method:`GlobalCache.compare_and_swap`."""

    def future_info(self, key, value):  # type:ignore[override]
        """Generate info string for Future."""

def is_locked_value(value):
    """Check if the given value is the special reserved value for key lock.

    Returns:
        bool: Whether the value is the special reserved value for key lock.
    """

def global_cache_key(key):
    """Convert Datastore key to ``bytes`` to use for global cache key.

    Args:
        key (datastore.Key): The Datastore key.

    Returns:
        bytes: The cache key.
    """
