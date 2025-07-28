"""Provides a tasklet decorator and related helpers.

Tasklets are a way to write concurrently running functions without threads.
Tasklets are executed by an event loop and can suspend themselves blocking for
I/O or some other operation using a yield statement. The notion of a blocking
operation is abstracted into the Future class, but a tasklet may also yield an
RPC in order to wait for that RPC to complete.

The @tasklet decorator wraps generator function so that when it is called, a
Future is returned while the generator is executed by the event loop. Within
the tasklet, any yield of a Future waits for and returns the Future's result.
For example::

    from from google.cloud.ndb.tasklets import tasklet

    @tasklet
    def foo():
        a = yield <AFuture>
        b = yield <BFuture>
        return a + b

    def main():
        f = foo()
        x = f.result()
        print(x)

In this example, `foo` needs the results of two futures, `AFuture` and
`BFuture`, which it gets somehow, for example as results of calls.
Rather than waiting for their values and blocking, it yields. First,
the tasklet yields `AFuture`.  The event loop gets `AFuture` and takes
care of waiting for its result.  When the event loop gets the result
of `AFuture`, it sends it to the tasklet by calling `send` on the
iterator returned by calling the tasklet.  The tasklet assigns the
value sent to `a` and then yields `BFuture`.  Again the event loop
waits for the result of `BFuture` and sends it to the tasklet.  The
tasklet then has what it needs to compute a result.

The tasklet simply returns its result. (Behind the scenes, when you
return a value from a generator in Python 3, a `StopIteration`
exception is raised with the return value as its argument. The event
loop catches the exception and uses the exception argument as the
result of the tasklet.)

Note that blocking until the Future's result is available using result() is
somewhat inefficient (though not vastly -- it is not busy-waiting). In most
cases such code should be rewritten as a tasklet instead::

    @tasklet
    def main_tasklet():
        f = foo()
        x = yield f
        print(x)

Calling a tasklet automatically schedules it with the event loop::

    def main():
        f = main_tasklet()
        eventloop.run()  # Run until no tasklets left to do
        f.done()  # Returns True
"""

from typing import Any

class Future:
    """Represents a task to be completed at an unspecified time in the future.

    This is the abstract base class from which all NDB ``Future`` classes are
    derived. A future represents a task that is to be performed
    asynchronously with the current flow of program control.

    Provides interface defined by :class:`concurrent.futures.Future` as well as
    that of the legacy Google App Engine NDB ``Future`` class.
    """

    info: Any
    def __init__(self, info: str = ...) -> None: ...
    def done(self):
        """Get whether future has finished its task.

        Returns:
            bool: True if task has finished, False otherwise.
        """

    def running(self):
        """Get whether future's task is still running.

        Returns:
            bool: False if task has finished, True otherwise.
        """

    def wait(self) -> None:
        """Wait for this future's task to complete.

        This future will be done and will have either a result or an exception
        after a call to this method.
        """

    def check_success(self) -> None:
        """Check whether a future has completed without raising an exception.

        This will wait for the future to finish its task and will then raise
        the future's exception, if there is one, or else do nothing.
        """

    def set_result(self, result) -> None:
        """Set the result for this future.

        Signals that this future has completed its task and sets the result.

        Should not be called from user code.
        """

    def set_exception(self, exception) -> None:
        """Set an exception for this future.

        Signals that this future's task has resulted in an exception. The
        future is considered done but has no result. Once the exception is set,
        calls to :meth:`done` will return True, and calls to :meth:`result`
        will raise the exception.

        Should not be called from user code.

        Args:
            exception (Exception): The exception that was raised.
        """

    def result(self):
        """Return the result of this future's task.

        If the task is finished, this will return immediately. Otherwise, this
        will block until a result is ready.

        Returns:
            Any: The result
        """
    get_result: Any
    def exception(self):
        """Get the exception for this future, if there is one.

        If the task has not yet finished, this will block until the task has
        finished. When the task has finished, this will get the exception
        raised during the task, or None, if no exception was raised.

        Returns:
            Union[Exception, None]: The exception, or None.
        """
    get_exception: Any
    def get_traceback(self):
        """Get the traceback for this future, if there is one.

        Included for backwards compatibility with legacy NDB. If there is an
        exception for this future, this just returns the ``__traceback__``
        attribute of that exception.

        Returns:
            Union[types.TracebackType, None]: The traceback, or None.
        """

    def add_done_callback(self, callback) -> None:
        """Add a callback function to be run upon task completion. Will run
        immediately if task has already finished.

        Args:
            callback (Callable): The function to execute.
        """

    def cancel(self) -> None:
        """Attempt to cancel the task for this future.

        If the task has already completed, this call will do nothing.
        Otherwise, this will attempt to cancel whatever task this future is
        waiting on. There is no specific guarantee the underlying task will be
        cancelled.
        """

    def cancelled(self):
        """Get whether the task for this future has been cancelled.

        Returns:
            :data:`True`: If this future's task has been cancelled, otherwise
                :data:`False`.
        """

    @staticmethod
    def wait_any(futures):
        """Calls :func:`wait_any`."""

    @staticmethod
    def wait_all(futures):
        """Calls :func:`wait_all`."""

class _TaskletFuture(Future):
    """A future which waits on a tasklet.

    A future of this type wraps a generator derived from calling a tasklet. A
    tasklet's generator is expected to yield future objects, either an instance
    of :class:`Future` or :class:`_remote.RemoteCall`. The result of each
    yielded future is then sent back into the generator until the generator has
    completed and either returned a value or raised an exception.

    Args:
        typing.Generator[Union[tasklets.Future, _remote.RemoteCall], Any, Any]:
            The generator.
    """

    generator: Any
    context: Any
    waiting_on: Any
    def __init__(self, generator, context, info: str = ...) -> None: ...
    def cancel(self) -> None:
        """Overrides :meth:`Future.cancel`."""

class _MultiFuture(Future):
    """A future which depends on multiple other futures.

    This future will be done when either all dependencies have results or when
    one dependency has raised an exception.

    Args:
        dependencies (typing.Sequence[tasklets.Future]): A sequence of the
            futures this future depends on.
    """

    def __init__(self, dependencies) -> None: ...
    def cancel(self) -> None:
        """Overrides :meth:`Future.cancel`."""

def tasklet(wrapped):
    """
    A decorator to turn a function or method into a tasklet.

    Calling a tasklet will return a :class:`~Future` instance which can be used
    to get the eventual return value of the tasklet.

    For more information on tasklets and cooperative multitasking, see the main
    documentation.

    Args:
        wrapped (Callable): The wrapped function.
    """

def wait_any(futures):
    """Wait for any of several futures to finish.

    Args:
        futures (typing.Sequence[Future]): The futures to wait on.

    Returns:
        Future: The first future to be found to have finished.
    """

def wait_all(futures) -> None:
    """Wait for all of several futures to finish.

    Args:
        futures (typing.Sequence[Future]): The futures to wait on.
    """

class Return(Exception):
    """Return from a tasklet in Python 2.

    In Python 2, generators may not return a value. In order to return a value
    from a tasklet, then, it is necessary to raise an instance of this
    exception with the return value::

        from google.cloud import ndb

        @ndb.tasklet
        def get_some_stuff():
            future1 = get_something_async()
            future2 = get_something_else_async()
            thing1, thing2 = yield future1, future2
            result = compute_result(thing1, thing2)
            raise ndb.Return(result)

    In Python 3, you can simply return the result::

        @ndb.tasklet
        def get_some_stuff():
            future1 = get_something_async()
            future2 = get_something_else_async()
            thing1, thing2 = yield future1, future2
            result = compute_result(thing1, thing2)
            return result

    Note that Python 2 is no longer supported by the newest versions of Cloud NDB.
    """

def sleep(seconds):
    """Sleep some amount of time in a tasklet.
    Example:
        ..code-block:: python
            yield tasklets.sleep(0.5)  # Sleep for half a second.
    Arguments:
        seconds (float): Amount of time, in seconds, to sleep.
    Returns:
        Future: Future will be complete after ``seconds`` have elapsed.
    """

def add_flow_exception(*args, **kwargs) -> None: ...
def make_context(*args, **kwargs) -> None: ...
def make_default_context(*args, **kwargs) -> None: ...

class QueueFuture:
    def __init__(self, *args, **kwargs) -> None: ...

class ReducingFuture:
    def __init__(self, *args, **kwargs) -> None: ...

class SerialQueueFuture:
    def __init__(self, *args, **kwargs) -> None: ...

def set_context(*args, **kwargs) -> None: ...
def synctasklet(wrapped):
    """A decorator to run a tasklet as a function when called.

    Use this to wrap a request handler function that will be called by some
    web application framework (e.g. a Django view function or a
    webapp.RequestHandler.get method).

    Args:
        wrapped (Callable): The wrapped function.
    """

def toplevel(wrapped):
    """A synctasklet decorator that flushes any pending work.

    Use of this decorator is largely unnecessary, as you should be using
    :meth:`~google.cloud.ndb.client.Client.context` which also flushes pending
    work when exiting the context.

    Args:
        wrapped (Callable): The wrapped function."
    """
