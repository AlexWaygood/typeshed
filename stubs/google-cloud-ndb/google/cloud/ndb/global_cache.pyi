"""GlobalCache interface and its implementations."""

import abc
from _typeshed import Incomplete
from typing import Any
from typing_extensions import Self

ConnectionError: Any

class GlobalCache(metaclass=abc.ABCMeta):
    """Abstract base class for a global entity cache.

    A global entity cache is shared across contexts, sessions, and possibly
    even servers. A concrete implementation is available which uses Redis.

    Essentially, this class models a simple key/value store where keys and
    values are arbitrary ``bytes`` instances. "Compare and swap", aka
    "optimistic transactions" should also be supported.

    Concrete implementations can either by synchronous or asynchronous.
    Asynchronous implementations should return
    :class:`~google.cloud.ndb.tasklets.Future` instances whose eventual results
    match the return value described for each method. Because coordinating with
    the single threaded event model used by ``NDB`` can be tricky with remote
    services, it's not recommended that casual users write asynchronous
    implementations, as some specialized knowledge is required.

    Attributes:
        strict_read (bool): If :data:`False`, transient errors that occur as part of a
            entity lookup operation will be logged as warnings but not raised to the
            application layer. If :data:`True`, in the event of transient errors, cache
            operations will be retried a number of times before eventually raising the
            transient error to the application layer, if it does not resolve after
            retrying. Setting this to :data:`True` will cause NDB operations to take
            longer to complete if there are transient errors in the cache layer.
        strict_write (bool): If :data:`False`, transient errors that occur as part of
            a put or delete operation will be logged as warnings, but not raised to the
            application layer. If :data:`True`, in the event of transient errors, cache
            operations will be retried a number of times before eventually raising the
            transient error to the application layer if it does not resolve after
            retrying. Setting this to :data:`False` somewhat increases the risk
            that other clients might read stale data from the cache. Setting this to
            :data:`True` will cause NDB operations to take longer to complete if there
            are transient errors in the cache layer.
    """

    __metaclass__: Any
    transient_errors: Any
    strict_read: bool
    strict_write: bool
    @abc.abstractmethod
    def get(self, keys):
        """Retrieve entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to get.

        Returns:
            List[Union[bytes, None]]]: Serialized entities, or :data:`None`,
                for each key.
        """

    @abc.abstractmethod
    def set(self, items, expires: Incomplete | None = ...):
        """Store entities in the cache.

        Arguments:
            items (Dict[bytes, Union[bytes, None]]): Mapping of keys to
                serialized entities.
            expires (Optional[float]): Number of seconds until value expires.

        Returns:
            Optional[Dict[bytes, Any]]: May return :data:`None`, or a `dict` mapping
                keys to arbitrary results. If the result for a key is an instance of
                `Exception`, the result will be raised as an exception in that key's
                future.
        """

    @abc.abstractmethod
    def delete(self, keys):
        """Remove entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to remove.
        """

    @abc.abstractmethod
    def watch(self, items):
        """Begin an optimistic transaction for the given items.

        A future call to :meth:`compare_and_swap` will only set values for keys
        whose values haven't changed since the call to this method. Values are used to
        check that the watched value matches the expected value for a given key.

        Arguments:
            items (Dict[bytes, bytes]): The items to watch.
        """

    @abc.abstractmethod
    def unwatch(self, keys):
        """End an optimistic transaction for the given keys.

        Indicates that value for the key wasn't found in the database, so there will not
        be a future call to :meth:`compare_and_swap`, and we no longer need to watch
        this key.

        Arguments:
            keys (List[bytes]): The keys to watch.
        """

    @abc.abstractmethod
    def compare_and_swap(self, items, expires: Incomplete | None = ...):
        """Like :meth:`set` but using an optimistic transaction.

        Only keys whose values haven't changed since a preceding call to
        :meth:`watch` will be changed.

        Arguments:
            items (Dict[bytes, Union[bytes, None]]): Mapping of keys to
                serialized entities.
            expires (Optional[float]): Number of seconds until value expires.

        Returns:
            Dict[bytes, bool]: A mapping of key to result. A key will have a result of
                :data:`True` if it was changed successfully.
        """

    @abc.abstractmethod
    def clear(self):
        """Clear all keys from global cache.

        Will be called if there previously was a connection error, to prevent clients
        from reading potentially stale data from the cache.
        """

class _InProcessGlobalCache(GlobalCache):
    """Reference implementation of :class:`GlobalCache`.

    Not intended for production use. Uses a single process wide dictionary to
    keep an in memory cache. For use in testing and to have an easily grokkable
    reference implementation. Thread safety is potentially a little sketchy.
    """

    cache: Any
    def __init__(self) -> None: ...
    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""

    def set(self, items, expires: Incomplete | None = ...) -> None:
        """Implements :meth:`GlobalCache.set`."""

    def delete(self, keys) -> None:
        """Implements :meth:`GlobalCache.delete`."""

    def watch(self, items) -> None:
        """Implements :meth:`GlobalCache.watch`."""

    def unwatch(self, keys) -> None:
        """Implements :meth:`GlobalCache.unwatch`."""

    def compare_and_swap(self, items, expires: Incomplete | None = ...):
        """Implements :meth:`GlobalCache.compare_and_swap`."""

    def clear(self) -> None:
        """Implements :meth:`GlobalCache.clear`."""

class RedisCache(GlobalCache):
    """Redis implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Redis
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        redis (redis.Redis): Instance of Redis client to use.
        strict_read (bool): If :data:`False`, connection errors during read operations
            will be logged with a warning and treated as cache misses, but will not
            raise an exception in the application, with connection errors during reads
            being treated as cache misses. If :data:`True`, in the event of connection
            errors, cache operations will be retried a number of times before eventually
            raising the connection error to the application layer, if it does not
            resolve after retrying. Setting this to :data:`True` will cause NDB
            operations to take longer to complete if there are transient errors in the
            cache layer. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an exception in
            the application. If :data:`True`, connection errors during write will be
            raised as exceptions in the application. Because write operations involve
            cache invalidation, setting this to :data:`False` may allow other clients to
            retrieve stale data from the cache. If :data:`True`, in the event of
            connection errors, cache operations will be retried a number of times before
            eventually raising the connection error to the application layer, if it does
            not resolve after retrying. Setting this to :data:`True` will cause NDB
            operations to take longer to complete if there are transient errors in the
            cache layer. Default: :data:`True`.
    """

    transient_errors: Any
    @classmethod
    def from_environment(cls, strict_read: bool = ..., strict_write: bool = ...) -> Self:
        """Generate a class:`RedisCache` from an environment variable.

        This class method looks for the ``REDIS_CACHE_URL`` environment
        variable and, if it is set, passes its value to ``Redis.from_url`` to
        construct a ``Redis`` instance which is then used to instantiate a
        ``RedisCache`` instance.

        Args:
            strict_read (bool): If :data:`False`, connection errors during read
                operations will be logged with a warning and treated as cache misses,
                but will not raise an exception in the application, with connection
                errors during reads being treated as cache misses. If :data:`True`, in
                the event of connection errors, cache operations will be retried a
                number of times before eventually raising the connection error to the
                application layer, if it does not resolve after retrying. Setting this
                to :data:`True` will cause NDB operations to take longer to complete if
                there are transient errors in the cache layer. Default: :data:`False`.
            strict_write (bool): If :data:`False`, connection errors during write
                operations will be logged with a warning, but will not raise an
                exception in the application. If :data:`True`, connection errors during
                write will be raised as exceptions in the application. Because write
                operations involve cache invalidation, setting this to :data:`False` may
                allow other clients to retrieve stale data from the cache. If
                :data:`True`, in the event of connection errors, cache operations will
                be retried a number of times before eventually raising the connection
                error to the application layer, if it does not resolve after retrying.
                Setting this to :data:`True` will cause NDB operations to take longer to
                complete if there are transient errors in the cache layer.  Default:
                :data:`True`.

        Returns:
            Optional[RedisCache]: A :class:`RedisCache` instance or
                :data:`None`, if ``REDIS_CACHE_URL`` is not set in the
                environment.
        """
    redis: Any
    strict_read: Any
    strict_write: Any
    def __init__(self, redis, strict_read: bool = ..., strict_write: bool = ...) -> None: ...
    @property
    def pipes(self): ...
    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""

    def set(self, items, expires: Incomplete | None = ...) -> None:
        """Implements :meth:`GlobalCache.set`."""

    def delete(self, keys) -> None:
        """Implements :meth:`GlobalCache.delete`."""

    def watch(self, items) -> None:
        """Implements :meth:`GlobalCache.watch`."""

    def unwatch(self, keys) -> None:
        """Implements :meth:`GlobalCache.watch`."""

    def compare_and_swap(self, items, expires: Incomplete | None = ...):
        """Implements :meth:`GlobalCache.compare_and_swap`."""

    def clear(self) -> None:
        """Implements :meth:`GlobalCache.clear`."""

class MemcacheCache(GlobalCache):
    """Memcache implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Memcache
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        client (pymemcache.Client): Instance of Memcache client to use.
        strict_read (bool): If :data:`False`, connection errors during read
            operations will be logged with a warning and treated as cache misses,
            but will not raise an exception in the application, with connection
            errors during reads being treated as cache misses. If :data:`True`, in
            the event of connection errors, cache operations will be retried a
            number of times before eventually raising the connection error to the
            application layer, if it does not resolve after retrying. Setting this
            to :data:`True` will cause NDB operations to take longer to complete if
            there are transient errors in the cache layer. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an
            exception in the application. If :data:`True`, connection errors during
            write will be raised as exceptions in the application. Because write
            operations involve cache invalidation, setting this to :data:`False` may
            allow other clients to retrieve stale data from the cache. If :data:`True`,
            in the event of connection errors, cache operations will be retried a number
            of times before eventually raising the connection error to the application
            layer, if it does not resolve after retrying.  Setting this to :data:`True`
            will cause NDB operations to take longer to complete if there are transient
            errors in the cache layer. Default: :data:`True`.
    """

    class KeyNotSet(Exception):
        key: Any
        def __init__(self, key) -> None: ...
        def __eq__(self, other): ...

    transient_errors: Any
    @classmethod
    def from_environment(cls, max_pool_size: int = ..., strict_read: bool = ..., strict_write: bool = ...) -> Self:
        """Generate a ``pymemcache.Client`` from an environment variable.

        This class method looks for the ``MEMCACHED_HOSTS`` environment
        variable and, if it is set, parses the value as a space delimited list of
        hostnames, optionally with ports. For example:

            "localhost"
            "localhost:11211"
            "1.1.1.1:11211 2.2.2.2:11211 3.3.3.3:11211"

        Args:
            max_pool_size (int): Size of connection pool to be used by client. If set to
                ``0`` or ``1``, connection pooling will not be used. Default: ``4``
            strict_read (bool): If :data:`False`, connection errors during read
                operations will be logged with a warning and treated as cache misses,
                but will not raise an exception in the application, with connection
                errors during reads being treated as cache misses. If :data:`True`, in
                the event of connection errors, cache operations will be retried a
                number of times before eventually raising the connection error to the
                application layer, if it does not resolve after retrying. Setting this
                to :data:`True` will cause NDB operations to take longer to complete if
                there are transient errors in the cache layer. Default: :data:`False`.
            strict_write (bool): If :data:`False`, connection errors during write
                operations will be logged with a warning, but will not raise an
                exception in the application. If :data:`True`, connection errors during
                write will be raised as exceptions in the application. Because write
                operations involve cache invalidation, setting this to :data:`False` may
                allow other clients to retrieve stale data from the cache. If
                :data:`True`, in the event of connection errors, cache operations will
                be retried a number of times before eventually raising the connection
                error to the application layer, if it does not resolve after retrying.
                Setting this to :data:`True` will cause NDB operations to take longer to
                complete if there are transient errors in the cache layer. Default:
                :data:`True`.

        Returns:
            Optional[MemcacheCache]: A :class:`MemcacheCache` instance or
                :data:`None`, if ``MEMCACHED_HOSTS`` is not set in the
                environment.
        """
    client: Any
    strict_read: Any
    strict_write: Any
    def __init__(self, client, strict_read: bool = ..., strict_write: bool = ...) -> None: ...
    @property
    def caskeys(self): ...
    def get(self, keys):
        """Implements :meth:`GlobalCache.get`."""

    def set(self, items, expires: Incomplete | None = ...):
        """Implements :meth:`GlobalCache.set`."""

    def delete(self, keys) -> None:
        """Implements :meth:`GlobalCache.delete`."""

    def watch(self, items) -> None:
        """Implements :meth:`GlobalCache.watch`."""

    def unwatch(self, keys) -> None:
        """Implements :meth:`GlobalCache.unwatch`."""

    def compare_and_swap(self, items, expires: Incomplete | None = ...):
        """Implements :meth:`GlobalCache.compare_and_swap`."""

    def clear(self) -> None:
        """Implements :meth:`GlobalCache.clear`."""
