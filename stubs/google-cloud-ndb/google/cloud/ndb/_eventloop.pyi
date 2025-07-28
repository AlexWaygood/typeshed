"""Event loop for running callbacks.

This should handle both asynchronous ``ndb`` objects and arbitrary callbacks.
"""

from typing import Any, NamedTuple

class _Event(NamedTuple):
    """_Event(when, callback, args, kwargs)"""

    when: Any
    callback: Any
    args: Any
    kwargs: Any

class EventLoop:
    """An event loop.

    Instances of ``EventLoop`` are used to coordinate single threaded execution
    of tasks and RPCs scheduled asynchronously.

    Since the the ``EventLoop`` runs in the same thread as user code, it's best
    to think of it as running tasks "on demand". Generally, when some piece of
    code needs a result from a future, the future's
    :meth:`~tasklets.Future.wait` method will end up calling
    :meth:`~EventLoop.run1`, which will attempt to execute a single task that
    is queued in the loop. The future will continue to call
    :meth:`~EventLoop.run1` until one of the callbacks ultimately puts that
    future into it's ``done`` state, either by setting the result or setting an
    exception.

    The :meth:`~EventLoop.run` method, which consumes the entire queue before
    returning, is usually only run when the end of the containing context is
    reached. At this point, there can't be any code waiting for results from
    the event loop, so any tasks still queued on the loop at this point, are
    just being run without regard for their results. For example, a request
    handler for a web application might write some objects to Datastore. This
    makes sure those writes complete before we exit from the current context.

    Ultimately, all data flows from calls to gRPC. gRPC handles asynchronous
    API calls in its own handler thread, so we use a synchronized queue to
    coordinate with gRPC. When a future from a gRPC call is added with
    :meth:`~EventLoop.queue_rpc`, a done callback is added to the gRPC future
    which causes it to push itself onto the synchronized queue when it is
    finished, so we can process the result here in the event loop. From the
    finished gRPC call, results will flow back up through whatever series of
    other futures were waiting on those results and results derived from those
    results.

    Currently, these are the separate queues used by the event loop in the
    order they are checked by :meth:`~EventLoop.run1`. For each call to
    :meth:`~EventLoop.run1`, the first thing it finds is called:

        current: These callbacks are called first, if there are any. Currently
            this is used to schedule calls to
            :meth:`tasklets.TaskletFuture._advance_tasklet` when it's time to
            send a tasklet a value that it was previously waiting on.

        idlers: Effectively, these are the same as ``current``, but just get
            called afterwards. These currently are used for batching certain
            calls to the back end. For example, if you call
            :func:`_datastore_api.lookup`, a new batch is created, and the key
            you're requesting is added to it. Subsequent calls add keys to the
            same batch. When the batch is initialized, an idler is added to the
            event loop which issues a single Datastore Lookup call for the
            entire batch. Because the event loop is called "on demand", this
            means this idler won't get called until something needs a result
            out of the event loop, and the actual gRPC call is made at that
            time.

        queue: These are callbacks that are supposed to be run at (or after) a
            certain time. This is used by :function:`tasklets.sleep`.

        rpcs: If all other queues are empty, and we are waiting on results of a
            gRPC call, then we'll call :method:`queue.Queue.get` on the
            synchronized queue, :attr:`~EventLoop.rpc_results`, to get the next
            finished gRPC call. This is the only point where
            :method:`~EventLoop.run1` might block. If the only thing to do is
            wait for a gRPC call to finish, we may as well wait.

    Attributes:
        current (deque): a FIFO list of (callback, args, kwds). These callbacks
            run immediately when the eventloop runs. Used by tasklets to
            schedule calls to :meth:`tasklets.TaskletFuture._advance_tasklet`.
        idlers (deque): a FIFO list of (callback, args, kwds). These callbacks
            run only when no other RPCs need to be fired first. Used for
            batching calls to the Datastore back end.
        inactive (int): Number of consecutive idlers that were noops. Reset
            to 0 whenever work is done by any callback, not necessarily by an
            idler. Not currently used.
        queue (list): a sorted list of (absolute time in sec, callback, args,
            kwds), sorted by time. These callbacks run only after the said
            time. Used by :func:`tasklets.sleep`.
        rpcs (dict): a map from RPC to callback. Callback is called when the
            RPC finishes.
        rpc_results (queue.Queue): A synchronized queue used to coordinate with
            gRPC. As gRPC futures that we're waiting on are finished, they will
            get added to this queue and then processed by the event loop.
    """

    current: Any
    idlers: Any
    inactive: int
    queue: Any
    rpcs: Any
    rpc_results: Any
    def __init__(self) -> None: ...
    def clear(self) -> None:
        """Remove all pending events without running any."""

    def insort_event_right(self, event) -> None:
        """Insert event in queue with sorting.

        This function assumes the queue is already sorted by ``event.when`` and
        inserts ``event`` in the queue, maintaining the sort.

        For events with same `event.when`, new events are inserted to the
        right, to keep FIFO order.

        Args:
            event (_Event): The event to insert.
        """

    def call_soon(self, callback, *args, **kwargs) -> None:
        """Schedule a function to be called soon, without a delay.

        Arguments:
            callback (callable): The function to eventually call.
            *args: Positional arguments to be passed to callback.
            **kwargs: Keyword arguments to be passed to callback.
        """

    def queue_call(self, delay, callback, *args, **kwargs) -> None:
        """Schedule a function call at a specific time in the future.

        Arguments:
            delay (float): Time in seconds to delay running the callback.
                Times over a billion seconds are assumed to be absolute
                timestamps rather than delays.
            callback (callable): The function to eventually call.
            *args: Positional arguments to be passed to callback.
            **kwargs: Keyword arguments to be passed to callback.
        """

    def queue_rpc(self, rpc, callback) -> None:
        """Add a gRPC call to the queue.

        Args:
            rpc (:class:`_remote.RemoteCall`): The future for the gRPC
                call.
            callback (Callable[[:class:`_remote.RemoteCall`], None]):
                Callback function to execute when gRPC call has finished.

        gRPC handles its asynchronous calls in a separate processing thread, so
        we add our own callback to `rpc` which adds `rpc` to a synchronized
        queue when it has finished. The event loop consumes the synchronized
        queue and calls `callback` with the finished gRPC future.
        """

    def add_idle(self, callback, *args, **kwargs) -> None:
        """Add an idle callback.

        An idle callback is a low priority task which is executed when
        there aren't other events scheduled for immediate execution.

        An idle callback can return True, False or None. These mean:

        - None: remove the callback (don't reschedule)
        - False: the callback did no work; reschedule later
        - True: the callback did some work; reschedule soon

        If the callback raises an exception, the traceback is logged and
        the callback is removed.

        Arguments:
            callback (callable): The function to eventually call.
            *args: Positional arguments to be passed to callback.
            **kwargs: Keyword arguments to be passed to callback.
        """

    def run_idle(self):
        """Run one of the idle callbacks.

        Returns:
            bool: Indicates if an idle callback was called.
        """

    def run0(self):
        """Run one item (a callback or an RPC wait_any).

        Returns:
            float: A time to sleep if something happened (may be 0);
              None if all queues are empty.
        """

    def run1(self):
        """Run one item (a callback or an RPC wait_any) or sleep.

        Returns:
            bool: True if something happened; False if all queues are empty.
        """

    def run(self) -> None:
        """Run until there's nothing left to do."""
