from .context import Context as _Context

class AsyncContext(_Context):
    """
    Async Context for storing segments.

    Inherits nearly everything from the main Context class.
    Replaces threading.local with a task based local storage class,
    Also overrides clear_trace_entities
    """

    def __init__(self, *args, loop=None, use_task_factory: bool = True, **kwargs) -> None: ...
    def clear_trace_entities(self) -> None:
        """
        Clear all trace_entities stored in the task local context.
        """

class TaskLocalStorage:
    """
    Simple task local storage
    """

    def __init__(self, loop=None) -> None: ...
    def __setattr__(self, name: str, value) -> None: ...
    def __getattribute__(self, item: str): ...
    def clear(self) -> None: ...

def task_factory(loop, coro):
    """
    Task factory function

    Fuction closely mirrors the logic inside of
    asyncio.BaseEventLoop.create_task. Then if there is a current
    task and the current task has a context then share that context
    with the new task
    """
